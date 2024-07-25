from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from scraper import scrape
import requests
from bs4 import BeautifulSoup

@tool
def search(term: str) -> str:
    """Search for user made websites"""
    return scrape(term)

@tool
def scrape(term: str) -> str:
    """Scrape a url"""
    r = requests.get(term)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup.get_text()

tools = [search, scrape]
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Make sure to use the search and scrape tool to for information."
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)
llm = Ollama(model="llama3")
agent = create_tool_calling_agent(tools, llm, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def ask(question):
    return agent_executor.invoke(
        {"input": question}
    )