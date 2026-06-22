"""Tools the agent can call: customer lookup (SQLite), plan details, roaming cost estimate."""
import os
import sqlite3
from langchain_core.tools import tool

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(HERE, 'data', 'telecom.db')

PLANS = {
    'Starter': {'price': 5, 'data': '5 GB', 'roaming_gb': 0},
    'Smart': {'price': 15, 'data': '25 GB', 'roaming_gb': 0},
    'Unlimited Basic': {'price': 30, 'data': 'unlimited (5 Mbps after 100 GB)', 'roaming_gb': 0},
    'Unlimited Pro': {'price': 50, 'data': 'unlimited', 'roaming_gb': 10},
}
ROAMING_PASS_PER_DAY = 5


@tool
def lookup_customer(customer_id: str) -> str:
    """Look up a customer by ID (e.g. C001): name, plan, data used, balance, and bill due date."""
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    r = con.execute('SELECT * FROM customers WHERE id=?', (customer_id.strip().upper(),)).fetchone()
    con.close()
    if not r:
        return f'No customer with id {customer_id}.'
    return (f"{r['name']} (id {r['id']}): plan={r['plan']}, data_used={r['data_used_gb']} GB, "
            f"balance=${r['balance_usd']}, bill_due={r['bill_due']}.")


@tool
def get_plan_details(plan_name: str) -> str:
    """Get price, data allowance, and included roaming for a plan
    (Starter, Smart, Unlimited Basic, Unlimited Pro)."""
    p = PLANS.get(plan_name.strip())
    if not p:
        return f'Unknown plan {plan_name}. Plans: {", ".join(PLANS)}.'
    return f"{plan_name}: ${p['price']}/mo, data={p['data']}, roaming_included={p['roaming_gb']} GB."


@tool
def roaming_cost(plan_name: str, days: int) -> str:
    """Estimate roaming cost for a plan over a number of days abroad."""
    p = PLANS.get(plan_name.strip())
    if not p:
        return f'Unknown plan {plan_name}.'
    if p['roaming_gb'] > 0:
        return (f"{plan_name} includes {p['roaming_gb']} GB roaming, so {days} days cost $0 within "
                f"that allowance.")
    return (f"{plan_name} has no included roaming; a pass is ${ROAMING_PASS_PER_DAY}/day, "
            f"so {days} days = ${ROAMING_PASS_PER_DAY * days}.")
