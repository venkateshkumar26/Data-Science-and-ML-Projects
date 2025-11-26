from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone as PineconeClient
from app.config import *

embedder = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

pc = PineconeClient(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX)



def create_vector_store(chunks, pdf_id):
    namespace = f"pdf_{pdf_id}"

    texts = [chunk.page_content for chunk in chunks]
    metadatas = [chunk.metadata for chunk in chunks]

    vector_store = PineconeVectorStore(
        index=index,
        embedding=embedder,
        namespace=namespace,
        text_key="text"
    )

    vector_store.add_texts(texts=texts, metadatas=metadatas)

    return vector_store


def load_vector_store(pdf_id):
    namespace = f"pdf_{pdf_id}"

    vector_store = PineconeVectorStore(
        index=index,
        embedding=embedder,
        namespace=namespace,
        text_key="text",
    )

    return vector_store
