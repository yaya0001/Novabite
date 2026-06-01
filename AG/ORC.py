import requests
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain.tools import tool
from groq import Groq
load_dotenv("/home/yahya/Documents/novabite/Novabite/.env")
@tool("get_current_weather",description="get the weather for some city", return_direct=False)
def get_current_weather(location: str) -> str:
    """Get the current weather in a given location"""
    # Use the OpenWeatherMap API to get the current weather
    response = requests.get(f'https://wttr.in/{location}?format=j1')
    return response.json()
llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)
agent = create_agent(
    tools=[get_current_weather],
    model=llm,
    system_prompt="You are a helpful assistant that can provide weather information in a funny way")
response=agent.invoke({"messages":[{"role":"user","content":"What's the weather like in cairo?"}]})
print(response['messages'][-1].content)








'''المستخدم يسأل
↓
Agent يفكر
↓
يقرر استخدام Tool
↓
Tool تجيب بيانات
↓
LLM يقرأ البيانات
↓
يصيغ رد مضحك
↓
LangChain يرجعه
↓
Python يطبعه'''

'''while not done:
   think()
   if tool_needed:
       run_tool()
   else:
       done = True'''