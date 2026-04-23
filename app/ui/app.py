import sys
import os
import requests
import streamlit as st
import json
from datetime import datetime

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT_DIR)

st.set_page_config(page_title="Research Assistant", layout="wide")

st.title("🔬 ScholarScope")
st.markdown("""
<div style="
    padding:15px;
    border-radius:10px;
    border:1px solid #1f2937;
    margin-bottom:15px;
">
<h4 style="margin-bottom:10px;"> What this app does</h4>
<p>
ScholarScope is an AI-powered Research Assistant that generates structured reviews from scientific papers using Retrieval-Augmented Generation (RAG).
</p>
<ul>
<li> Retrieves relevant research papers (from arXiv & Semantic Scholar)</li>
<li> Summarizes key insights</li> 
<li> Provides clickable references</li>
<li> Visualizes citation graphs</li>
</ul>
<p>
Choose <b>Research Query</b> to explore topics or <b>PDF Upload</b> to analyze documents.
</p>
</div>
""", unsafe_allow_html=True)


st.markdown("""
<style>
a {
    text-decoration: none;
    color: #00c6ff;
}
a:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)


#API_URL = "http://127.0.0.1:8000"
API_URL = "http://backend:8000"
HISTORY_FILE = "chat_history.json"

# ---------------- LOAD / SAVE ----------------
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

# ---------------- HELPER FUNCTION ----------------
def get_chat_type(chat):
    #  PRIORITY: chat-level type
    if "type" in chat:
        return chat["type"]

    #  Fallback for old chats
    messages = chat.get("messages", [])
    if messages:
        first_msg = messages[0]
        if first_msg.get("type") == "pdf":
            return "PDF Upload"
        else:
            return "Research Query"

    return "Research Query"

# ---------------- SESSION STATE ----------------
if "history" not in st.session_state:
    st.session_state.history = load_history()

if "current_chat" not in st.session_state:
    st.session_state.current_chat = []

if "current_chat_index" not in st.session_state:
    st.session_state.current_chat_index = None

# ---------------- MODE (MOVED UP) ----------------
mode = st.sidebar.selectbox(
    "Choose Mode",
    ["Research Query", "PDF Upload"]
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("📂 Chats")

search_query = st.sidebar.text_input("🔍 Search chats")

if st.sidebar.button("➕ New Chat"):
    st.session_state.current_chat = []
    st.session_state.current_chat_index = None

# ---------------- DISPLAY CHATS (FILTERED) ----------------
for i, chat in enumerate(st.session_state.history):

    chat_type = get_chat_type(chat)

    #  FILTER BY MODE
    if chat_type != mode:
        continue

    chat_name = chat.get("name", f"Chat {i+1}")
    timestamp = chat.get("timestamp", "")

    if search_query and search_query.lower() not in chat_name.lower():
        continue

    col1, col2 = st.sidebar.columns([4, 1])

    # Optional label
    label = "📄" if chat_type == "PDF Upload" else "🔍"

    if col1.button(f"{label} {chat_name} ({timestamp})", key=f"load_{i}"):
        st.session_state.current_chat = chat["messages"].copy()
        st.session_state.current_chat_index = i

    if col2.button("❌", key=f"delete_{i}"):
        st.session_state.history.pop(i)
        save_history(st.session_state.history)
        st.session_state.current_chat = []
        st.session_state.current_chat_index = None
        st.rerun()

if st.sidebar.button("🗑️ Delete All History"):
    st.session_state.history = []
    save_history([])
    st.session_state.current_chat = []
    st.session_state.current_chat_index = None
    st.sidebar.success("All history deleted")

# ---------------- RENAME CHAT ----------------
if st.session_state.current_chat_index is not None:
    new_name = st.sidebar.text_input(
        "✏️ Rename Chat",
        value=st.session_state.history[st.session_state.current_chat_index].get("name", "")
    )

    if st.sidebar.button("Save Name"):
        st.session_state.history[st.session_state.current_chat_index]["name"] = new_name
        save_history(st.session_state.history)
        st.sidebar.success("Renamed!")

# ---------------- RESEARCH QUERY ----------------
if mode == "Research Query":

    st.subheader("💬 Chat")

    for chat in st.session_state.current_chat:
        with st.chat_message("user"):
            st.write(chat["query"])
        with st.chat_message("assistant"):
            st.write(chat["result"])

            # SHOW REFERENCES
            sources = chat.get("sources", [])
            if sources:
                st.markdown("### 📚 References")
                for i, paper in enumerate(sources, 1):
                    title = paper.get("title", "Untitled")
                    link = paper.get("link", "")

                    if link:
                        st.markdown(f"{i}. [{title}]({link})")
                    else:
                        st.markdown(f"{i}. {title}")

            # SHOW GRAPH (FROM SAVED HTML)
            graph_html = chat.get("graph_html")
            if graph_html:
                st.markdown("### 🕸️ Citation Graph")
                st.components.v1.html(graph_html, height=600, scrolling=True)


    query = st.chat_input("Ask a research question...")

    if query:
        with st.chat_message("user"):
            st.write(query)

        with st.chat_message("assistant"):
            with st.spinner("Thinking... ⏳"):
                try:
                    response = requests.get(
                        f"{API_URL}/research",
                        params={"query": query}
                    )
                    data = response.json()

                    if "error" in data:
                        result = data["error"]
                        st.error(result)
                    else:
                        result = data.get("result", "No result found")
                        sources = data.get("sources", [])
                        graph_path = data.get("graph_path", None)
                        graph_html = None
                        if graph_path and os.path.exists(graph_path):
                            try:
                                with open(graph_path, "r", encoding="utf-8") as f:
                                    graph_html = f.read()
                            except:
                                graph_html = None

                        # ---------------- RESULT ----------------
                        st.markdown("### 📄 Result")
                        #st.write(result)
                        st.markdown(result)

                        # ---------------- REFERENCES ----------------
                        if sources:
                            st.markdown("### 📚 References")

                            for i, paper in enumerate(sources, 1):
                                title = paper.get("title", "Untitled")
                                link = paper.get("link", "")

                                if link:
                                    st.markdown(f"{i}. [{title}]({link})")
                                else:
                                    st.markdown(f"{i}. {title}")

                        # ---------------- CITATION GRAPH ----------------
                        graph_html = None

                        #  Load graph HTML (only once when API returns it)
                        if graph_path and os.path.exists(graph_path):
                            try:
                                with open(graph_path, "r", encoding="utf-8") as f:
                                    graph_html = f.read()
                            except Exception as e:
                                st.warning(f"Graph could not be loaded: {e}")

                        #  Display graph
                        if graph_html:
                            st.markdown("### 🕸️ Citation Graph")
                            st.components.v1.html(graph_html, height=600, scrolling=True)


                except Exception as e:
                    result = f"API Error: {e}"
                    st.error(result)

        st.session_state.current_chat.append({
            "type": "query",
            "query": query,
            "result": result,
            "sources": sources,
            "graph_html": graph_html
        })

    if st.button("💾 Save Chat"):
        if st.session_state.current_chat:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

            chat_data = {
                "type": "Research Query",   
                "name": f"Chat {len(st.session_state.history)+1}",
                "timestamp": timestamp,
                "messages": st.session_state.current_chat.copy()
            }


            st.session_state.history.append(chat_data)
            save_history(st.session_state.history)

            st.success("Chat saved!")

# ---------------- PDF UPLOAD ----------------
elif mode == "PDF Upload":

    st.subheader("📄 PDF Chat")

    for chat in st.session_state.current_chat:
        if chat.get("type") == "pdf":
            with st.chat_message("user"):
                st.write(f"📄 Uploaded: {chat['file_name']}")
            with st.chat_message("assistant"):
                st.write(chat["result"])

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_file is not None:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())

        if st.button("Analyze PDF"):
            with st.spinner("Analyzing... ⏳"):
                try:
                    from app.pipelines.pdf_pipeline import run_pdf_pipeline

                    result = run_pdf_pipeline("temp.pdf")

                    with st.chat_message("user"):
                        st.write(f"📄 Uploaded: {uploaded_file.name}")

                    with st.chat_message("assistant"):
                        st.write(result)

                    st.session_state.current_chat.append({
                        "type": "pdf",
                        "file_name": uploaded_file.name,
                        "result": result
                    })

                except Exception as e:
                    st.error(f"Error: {e}")

    if st.button("💾 Save PDF Chat"):
        if st.session_state.current_chat:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

            chat_data = {
                "type": "PDF Upload",   
                "name": f"PDF Chat {len(st.session_state.history)+1}",
                "timestamp": timestamp,
                "messages": st.session_state.current_chat.copy()
            }


            st.session_state.history.append(chat_data)
            save_history(st.session_state.history)

            st.success("PDF chat saved!")
