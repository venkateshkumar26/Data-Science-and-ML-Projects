import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000/generate"

st.title("AI PPT Generator")

title = st.text_input("Enter a project title:")

if st.button("Generate PPT"):
    if not title:
        st.error("Please enter a title")
    else:
        with st.spinner("Generating PPT from backend..."):
            response = requests.get(BACKEND_URL, params={"title": title})

            if response.status_code != 200:
                st.error("Backend error: " + response.text)
            else:
                ppt_bytes = response.content

                st.download_button(
                    label="Download PPT",
                    data=ppt_bytes,
                    file_name="generated.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                )
