from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from app.vector_store import load_vector_store
from app.config import LLM_MODEL
import os

def get_rag_pipeline(pdf_id):

    vector_store = load_vector_store(pdf_id)
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})

    prompt = ChatPromptTemplate.from_template("""
    You are an assistant for question-answering tasks.
    Use the following retrieved context to answer the question.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """)

    llm = ChatGroq(model=LLM_MODEL,api_key=os.getenv("GROQ_API_KEY"))

    rag_chain = (
    {
        "context": lambda x: retriever.invoke(x["question"]),
        "question": lambda x: x["question"]
    }
    | prompt
    | llm
    | StrOutputParser()
)

    return rag_chain



