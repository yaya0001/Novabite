from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from crewai import tool
import config
@tool
def get_retriever(string: str)->list[str]:
    """This function retrieves the vector store and returns a retriever object for querying."""
    embeddings = HuggingFaceEmbeddings(model_name=config.model_name)
    vector_store = FAISS.load_local(
        config.vdb_path,
        embeddings,
        allow_dangerous_deserialization=True
    )
    retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": config.top_k
    }
    )
    llm = ChatGroq(
    model=config.groq_model,
    temperature=config.temperature
    )
    prompt = ChatPromptTemplate.from_template(
    config.prompt
)


