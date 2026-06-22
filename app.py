"""Streamlit UI for the telecom ops assistant: ask a question, see the answer and the tool trace."""
import os
import sys
import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))
from agent import run   # noqa: E402

st.set_page_config(page_title='Telecom ops assistant', page_icon='📶', layout='centered')
st.title('📶 Telecom ops assistant')
st.caption('Ask about a customer (C001–C004). The agent looks up real records with tools, then answers.')

q = st.text_input(
    'Question',
    value='Customer C001 is traveling abroad for 5 days. Is roaming covered, and what is their balance?')

if q:
    with st.spinner('Looking up records...'):
        answer, trace = run(q)
    st.markdown('**Tools called**')
    st.code('  ->  '.join(trace) if trace else '(none)')
    st.markdown('**Answer**')
    st.success(answer)
