from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import config
#---------------------------------------------------------------------------------#
#Load Directory:
know_path=config.know_path
loader = DirectoryLoader(know_path,glob="*.md", loader_cls=TextLoader)
documents = loader.load()
#chunking:
text_splitter = RecursiveCharacterTextSplitter(chunk_size=config.chunk_size, chunk_overlap=config.chunk_overlap)
chunks = text_splitter.split_documents(documents)
#Embeddings:
embeddings = HuggingFaceEmbeddings(model_name=config.model_name)
#save to vectorstore:
vector_store = FAISS.from_documents(
    chunks,
    embeddings
)
#save vectorstore to disk:
try:
    vector_store.save_local(config.vdb_path)
except Exception as e:
    print(f"Error occurred while saving vector store: {e}")
