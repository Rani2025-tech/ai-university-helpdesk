import streamlit as st
import requests

API_URL = "http://localhost:8000/api"

st.set_page_config(
    page_title="AI University Helpdesk",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 AI University Helpdesk")
st.markdown("Ask any question about admissions, exams, hostel, placements, or campus services.")

col1, col2 = st.columns([3, 1])
with col2:
    language = st.selectbox(
        "🌐 Language",
        options=["auto", "en", "hi", "or"],
        format_func=lambda x: {
            "auto": "🌐 Auto-detect",
            "en": "🇬🇧 English",
            "hi": "🇮🇳 Hindi",
            "or": "🏛️ Odia"
        }[x]
    )

# ── Sidebar: PDF Upload ──────────────────────────────────────────
with st.sidebar:
    st.header("📄 Upload University PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        if st.button("Upload & Process"):
            with st.spinner("Uploading and processing PDF..."):
                try:
                    files    = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                    response = requests.post(f"{API_URL}/upload", files=files)

                    if response.status_code == 200:
                        data = response.json()
                        st.success(f"✅ {data['message']}")
                        st.info(f"📦 {data['chunks_created']} chunks created")
                    else:
                        st.error(f"❌ Upload failed: {response.json()['detail']}")
                except Exception as e:
                    st.error(f"❌ Could not connect to server: {str(e)}")

    st.divider()

    # List uploaded documents
    st.header("📚 Uploaded Documents")
    try:
        response = requests.get(f"{API_URL}/documents")
        if response.status_code == 200:
            data = response.json()
            if data["total"] == 0:
                st.info("No documents uploaded yet.")
            else:
                for doc in data["documents"]:
                    st.markdown(f"📄 {doc}")
    except:
        st.warning("⚠️ Server not reachable")

# ── Chat Interface ───────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a university question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
    f"{API_URL}/ask",
    json={"question": prompt, "language": language}
)

                if response.status_code == 200:
                    answer = response.json()["answer"]
                    st.markdown(answer)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })
                elif response.status_code == 400:
                    msg = response.json()["detail"]
                    st.warning(f"⚠️ {msg}")
                else:
                    st.error("❌ Something went wrong. Please try again.")

            except Exception as e:
                st.error(f"❌ Could not connect to server: {str(e)}")