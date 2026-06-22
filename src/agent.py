"""Tool-using telecom assistant.

An LLM router (JSON mode) extracts what the request needs; the tools are then called deterministically
in code, which grounds the answer in real data so the model cannot invent customer details; the LLM
composes the final answer from the tool results. Runs on a small local model via Ollama.
"""
import json
import os
import re
import sys
import ollama

sys.path.insert(0, os.path.dirname(__file__))
from tools import lookup_customer, get_plan_details, roaming_cost   # noqa: E402

MODEL = os.environ.get('AGENT_LLM', 'llama3.2:3b')

ROUTER = """You route telecom support requests. Output a JSON object with:
- customer_id: a customer id like "C001" if present, else null
- needs: list of any of ["plan", "roaming"] the request asks about
- days: number of days abroad if mentioned, else null
Output ONLY the JSON.

Request: {q}"""


def route(question):
    try:
        r = ollama.chat(model=MODEL, format='json', options={'temperature': 0},
                        messages=[{'role': 'user', 'content': ROUTER.format(q=question)}])
        return json.loads(r['message']['content'])
    except Exception:
        return {}


def run(question):
    p = route(question)
    ql = question.lower()

    cand = str(p.get('customer_id') or '')
    if re.match(r'^C\d{3}$', cand, re.I):
        cid = cand.upper()
    else:
        m = re.search(r'\bC\d{3}\b', question, re.I)
        cid = m.group(0).upper() if m else None

    needs = set(p.get('needs') or [])
    if any(w in ql for w in ['roam', 'abroad', 'travel', 'overseas']):
        needs.add('roaming')
    if any(w in ql for w in ['how much', 'price', ' cost', 'plan detail', 'which plan', 'what plan']):
        needs.add('plan')
    dm = re.search(r'(\d+)\s*day', ql)
    days = int(dm.group(1)) if dm else int(p.get('days') or 1)

    trace, facts, plan_name = [], [], None
    if cid:
        res = lookup_customer.invoke({'customer_id': cid})
        trace.append(f'lookup_customer({cid})')
        facts.append(res)
        pm = re.search(r'plan=([^,]+)', res)
        plan_name = pm.group(1).strip() if pm else None
    if 'plan' in needs and plan_name:
        res = get_plan_details.invoke({'plan_name': plan_name})
        trace.append(f'get_plan_details({plan_name})')
        facts.append(res)
    if 'roaming' in needs and plan_name:
        res = roaming_cost.invoke({'plan_name': plan_name, 'days': days})
        trace.append(f'roaming_cost({plan_name}, {days})')
        facts.append(res)

    context = '\n'.join(facts) if facts else 'No tool data available.'
    ans = ollama.chat(model=MODEL, options={'temperature': 0.1}, messages=[{'role': 'user', 'content':
        f'Question: {question}\n\nTool results:\n{context}\n\n'
        'Answer the question concisely using only the tool results above.'}])
    return ans['message']['content'].strip(), trace


if __name__ == '__main__':
    q = (sys.argv[1] if len(sys.argv) > 1
         else "Customer C001 is traveling abroad for 5 days. Is roaming covered, and what is their balance?")
    answer, trace = run(q)
    print('Q:', q)
    print('TRACE:', ' -> '.join(trace))
    print('A:', answer)
