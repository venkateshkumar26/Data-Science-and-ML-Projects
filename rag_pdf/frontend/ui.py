import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("Cloud RAG - PDF Question and Answering")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    if st.button("Upload PDF"):
        try:
            response = requests.post(
                f"{API_URL}/upload-pdf",
                files={"file": uploaded_file}
            )

            if response.status_code != 200:
                st.error(f"Upload failed: {response.text}")
            else:
                pdf_id = response.json()["pdf_id"]
                st.session_state["pdf_id"] = pdf_id
                st.success("PDF uploaded successfully!")

        except Exception as e:
            st.error(f"Error: {e}")

if "pdf_id" in st.session_state:
    query = st.text_input("Ask a question:")

    if st.button("Ask"):
        try:
            res = requests.post(
                f"{API_URL}/ask-pdf",
                json={   
                    "pdf_id": st.session_state["pdf_id"],
                    "question": query
                }
            )

            if res.status_code != 200:
                st.error(f"API Error: {res.text}")
            else:
                answer = res.json()["answer"]
                st.write(answer)

        except Exception as e:
            st.error(f"Error: {e}")

