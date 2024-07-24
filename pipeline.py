from langchain import hub
from langchain.agents import AgentExecutor, create_self_ask_with_search_agent
from langchain_community.llms import Ollama
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
prompt = hub.pull("hwchase17/self-ask-with-search")
llm = Ollama(model="llama3")
agent = create_self_ask_with_search_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
agent_executor.invoke(
    {"input": "Where can I check the status of webpages"}
)

