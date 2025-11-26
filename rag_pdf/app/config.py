import os

PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")
PINECONE_ENV='gcp-starter'
PINECONE_INDEX='pdf-768-index'

EMBEDDING_MODEL="sentence-transformers/all-mpnet-base-v2"
LLM_MODEL = "llama-3.1-8b-instant"
