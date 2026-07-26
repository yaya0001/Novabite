from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
load_dotenv("/home/yahya/Documents/novabite/Novabite/.env")
Rag_agent = Agent(role="It takes a question and a context and returns an answer based on the context.",
                  goal="To provide accurate and helpful answers based on the provided context.",
                  backstory="You are a helpful assistant that can provide information based on the provided context.",
                  llm=LLM("llama-3.1-8b-instant"), tools=["RAG"])