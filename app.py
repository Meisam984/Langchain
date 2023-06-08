import streamlit as st
from streamlit_chat import message

from src.utils import load_split_git_url, split_to_chunks, embed_upload_chunks
import os


openai_api_key = st.sidebar.text_input(
    label="🔑 Your OpenAI API key ⬇️⬇️⬇️",
    placeholder="Paste your openAI API key, sk-",
    type="password")

os.environ["OPENAI_API_KEY"] = openai_api_key

activeloop_token = st.sidebar.text_input(
    label="🔑 Your Activeloop Token ⬇️⬇️⬇️",
    placeholder="Paste your Activeloop Token",
    type="password")

os.environ['ACTIVELOOP_TOKEN'] = activeloop_token

root_URL = st.sidebar.text_input(
    label="🐱 Github Repository https URL ⬇️⬇️⬇️",
    placeholder="Paste the Github repo URL",
    type="password")

deeplake_account = st.sidebar.text_input(
    label="🔄 Deeplake Account name ⬇️⬇️⬇️",
    placeholder="Paste the Deeplake Account name",
    type="password")

docs = load_split_git_url(root_URL)
texts = split_to_chunks(docs)
db = embed_upload_chunks(texts, deeplake_account)







