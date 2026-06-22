"""FastAPI wrapping the assistant. POST /ask -> {answer, trace}."""
import os
import sys
from fastapi import FastAPI
from pydantic import BaseModel

sys.path.insert(0, os.path.dirname(__file__))
from agent import run   # noqa: E402

app = FastAPI(title='Telecom ops assistant')


class Ask(BaseModel):
    question: str


@app.post('/ask')
def ask(a: Ask):
    answer, trace = run(a.question)
    return {'answer': answer, 'trace': trace}
