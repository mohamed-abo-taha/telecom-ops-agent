"""Seed a small SQLite customer database that the agent's tools read from."""
import os
import sqlite3

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(HERE, 'data', 'telecom.db')

CUSTOMERS = [
    ('C001', 'Sara Ahmed', 'Unlimited Pro', 85.0, 12.0, '2026-07-14'),
    ('C002', 'Omar Khan', 'Smart', 22.0, 3.5, '2026-07-14'),
    ('C003', 'Lina Park', 'Unlimited Basic', 140.0, 0.0, '2026-07-14'),
    ('C004', 'Ali Hassan', 'Starter', 4.2, 1.0, '2026-07-14'),
]


def init():
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    con = sqlite3.connect(DB)
    con.execute('DROP TABLE IF EXISTS customers')
    con.execute('CREATE TABLE customers '
                '(id TEXT PRIMARY KEY, name TEXT, plan TEXT, data_used_gb REAL, '
                'balance_usd REAL, bill_due TEXT)')
    con.executemany('INSERT INTO customers VALUES (?,?,?,?,?,?)', CUSTOMERS)
    con.commit()
    con.close()
    return len(CUSTOMERS)


if __name__ == '__main__':
    print('seeded', init(), 'customers')
