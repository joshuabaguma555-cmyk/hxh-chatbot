import streamlit as st
from collections import deque
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

# =========================
# MEMORY (5–10 interactions)
# =========================
memory = deque(maxlen=10)

def add_memory(user, bot):
    memory.append((user, bot))

def get_memory():
    return "\n".join([f"User: {u}\nBot: {b}" for u, b in memory])

# =========================
# TEAM DATA
# =========================
team = [
    {"name":"Ahebwa Baguma Joshua","age":21,"level":"Undergraduate","university":"M'sila University","field":"Medicine"},
    {"name":"Nzimi Joel","age":22,"level":"Undergraduate","university":"M'sila University","field":"Not specified"},
    {"name":"Zia John Xavier","age":22,"level":"Undergraduate","university":"M'sila University","field":"Civil Engineering"},
    {"name":"Kamala Elton","age":21,"level":"Undergraduate","university":"M'sila University","field":"Civil Engineering"},
    {"name":"Mugwanya Vianny","age":23,"level":"Undergraduate","university":"M'sila University","field":"Medicine"},
    {"name":"Mohan Mohammed","age":22,"level":"Undergraduate","university":"M'sila University","field":"Civil Engineering"}
]

def get_team_info():
    return "\n".join([
        f"{t['name']} | {t['age']} | {t['level']} | {t['university']} | {t['field']}"
        for t in team
    ])

# =========================
# HUNTER X HUNTER DATA (RAG)
# =========================
docs = [
    Document(page_content="Gon Freecss is a hunter searching for his father."),
    Document(page_content="Killua Zoldyck is an assassin with lightning abilities."),
    Document(page_content="Kurapika seeks revenge for his clan."),
    Document(page_content="Hunter x Hunter involves strategy, battles, and Nen abilities.")
]

embedding = HuggingFaceEmbeddings()
db = Chroma.from_documents(docs, embedding)

# =========================
# DOMAIN FILTER
# =========================
def is_valid(query):
    q = query.lower()
    keywords = ["hunter", "gon", "killua", "kurapika", "nen", "team", "member"]
    return any(k in q for k in keywords)

# =========================
# RETRIEVER
# =========================
def retrieve(query):
    results = db.similarity_search(query, k=3)
    return "\n".join([r.page_content for r in results])

# =========================
# RESPONSE ENGINE
# =========================
def generate(query):

    # TEAM QUESTIONS
    if "team" in query.lower() or "member" in query.lower():
        return get_team_info()

    # HXH QUESTIONS (RAG)
    context = retrieve(query)

    return f"""
Question: {query}

Context:
{context}

Memory:
{get_memory()}

Answer:
This response is based on Hunter x Hunter knowledge.
"""

# =========================
# STREAMLIT UI
# =========================
st.title("🎯 HXH RAG Chatbot")

user_input = st.text_input("Ask a question:")

if st.button("Send"):
    if not is_valid(user_input):
        response = "I can only answer Hunter x Hunter or team-related questions."
    else:
        response = generate(user_input)

    add_memory(user_input, response)

    st.write("### 🤖 Response")
    st.write(response)

st.write("### 🧠 Memory")
st.write(get_memory())