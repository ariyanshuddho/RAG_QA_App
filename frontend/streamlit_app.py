import streamlit as st
import requests

st.set_page_config(page_title="🧠 RAG Assistant", layout="centered")

st.markdown("## 📄 Document Q&A Assistant")
st.caption("Ask questions about your documents using Retrieval-Augmented Generation (RAG).")

# Upload Section
st.markdown("### 📤 Upload a Document")
uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt", "jpg", "png", "csv", "db"])

if uploaded_file:
    with st.spinner("🔄 Uploading and processing..."):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        response = requests.post("http://127.0.0.1:8000/upload/", files=files)

        if response.status_code == 200:
            file_id = response.json()["file_id"]
            st.success("✅ File processed successfully!")
            st.session_state["file_id"] = file_id
            st.session_state["preview"] = response.json().get("text_preview", "")
        else:
            st.error(f"❌ Upload failed: {response.text}")
            st.stop()

# Preview Extracted Text
if "preview" in st.session_state:
    with st.expander("📖 Preview Extracted Text"):
        st.write(st.session_state["preview"])

# Question & Answer Section
if "file_id" in st.session_state:
    st.markdown("### ❓ Ask a Question")
    question = st.text_input("💬 What would you like to know about this document?")

    if st.button("🧠 Ask"):
        if not question.strip():
            st.warning("⚠️ Please enter a question.")
        else:
            with st.spinner("🤔 Thinking..."):
                payload = {"question": question, "file_id": st.session_state["file_id"]}
                res = requests.post("http://127.0.0.1:8000/query/", json=payload)

                if res.status_code == 200:
                    data = res.json()

                    # Show answer
                    st.markdown("### 💡 Answer")
                    st.success(data["answer"])

                    # Document type (optional)
                    if "document_type" in data:
                        st.markdown("### 🗂️ Document Type")
                        st.info(f"**{data['document_type']}**")

                    # Top matching chunks
                    with st.expander("🧩 Top Matching Chunks"):
                        for i, chunk in enumerate(data["top_chunks"], 1):
                            st.markdown(f"**Chunk {i}:**")
                            st.write(chunk)
                else:
                    st.error(f"❌ Query failed: {res.text}")

# Reset session button
if st.button("🔁 Clear & Upload Another Document"):
    st.session_state.clear()
    st.experimental_rerun()
