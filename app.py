import streamlit as st
from collections import deque

# =========================
# MEMORY (last 10 chats)
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
"Ahebwa Baguma Joshua | 21 | Undergraduate | M'sila University | Medicine",
"Nzimi Joel | 22 | Undergraduate | M'sila University | Not specified",
"Zia John Xavier | 22 | Undergraduate | M'sila University | Civil Engineering",
"Kamala Elton | 21 | Undergraduate | M'sila University | Civil Engineering",
"Mugwanya Vianny | 23 | Undergraduate | M'sila University | Medicine",
"Mohan Mohammed | 22 | Undergraduate | M'sila University | Civil Engineering"
]

# =========================
# HXH KNOWLEDGE
# =========================
knowledge = {
    "gon": "Gon Freecss is a hunter searching for his father.",
    "killua": "Killua Zoldyck is an assassin with lightning abilities.",
    "kurapika": "Kurapika seeks revenge for his clan.",
    "nen": "Nen is a technique that allows control of life energy."
}

# =========================
# DOMAIN FILTER
# =========================
def is_valid(query):
    q = query.lower()
    keywords = ["gon", "killua", "kurapika", "nen", "hunter", "team"]
    return any(k in q for k in keywords)

# =========================
# RESPONSE SYSTEM
# =========================
def generate(query):
    q = query.lower()

    if "team" in q:
        return "\n".join(team)

    for key in knowledge:
        if key in q:
            return knowledge[key]

    return "This question is outside Hunter x Hunter scope."

# =========================
# UI
# =========================
st.title("🎯 HXH Chatbot")

user_input = st.text_input("Ask a question:")

if st.button("Send"):
    if not is_valid(user_input):
        response = "I only answer Hunter x Hunter or team-related questions."
    else:
        response = generate(user_input)

    add_memory(user_input, response)

    st.write("### 🤖 Response")
    st.write(response)

st.write("### 🧠 Memory")
st.write(get_memory())
