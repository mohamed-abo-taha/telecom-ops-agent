# Telecom ops assistant — project spec

## What this is
A tool-using assistant for telecom operations. An LLM router decides what a request needs, the tools
run in code (so the answer is grounded in real data, not invented), and the LLM writes the final
answer from the tool results. Backed by a small local model (Llama-3.2 via Ollama), fully local, no
API keys.

## Tools (LangChain tools)
- lookup_customer(id): reads a customer record (plan, data used, balance, bill due) from SQLite.
- get_plan_details(plan): price, data allowance, included roaming.
- roaming_cost(plan, days): estimates roaming cost over N days.

## Flow
1. LLM router (JSON mode) extracts customer_id, needs (plan / roaming), and days, with regex and
   keyword guards as a deterministic backstop.
2. Code calls the tools in order: lookup_customer, then get_plan_details / roaming_cost using the
   customer's actual plan.
3. The LLM composes the answer from the tool results only. The response includes the tool-call trace.

## Why this design
A free ReAct loop on a small local model was unreliable (it mangled tool arguments and hallucinated).
Putting the orchestration in code and using the LLM only for routing and final wording makes it
reliable on a 3B model and removes the chance of invented customer data.

## Maps to the JD
GenAI frameworks (LangChain tools), tool use, prompt engineering, a FastAPI service for integration,
and multi-step problem solving over internal data.
