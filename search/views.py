from django.shortcuts import render
from django.http import JsonResponse
import requests
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from scraper import scrape
import requests
from bs4 import BeautifulSoup

def scrape(term):
    boogle = requests.get('https://boogle.boreal.express/search?q=' + term)
    boogl = BeautifulSoup(boogle.content, 'html.parser')
    results = boogl.find_all('a')
    results.pop(0)
    print(results)
    links = []
    for link in boogl.find_all('a'):
        l = link.get('href')
        if l not in links:
            links.append(l)
    return links[:4]
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
llm = OllamaFunctions(model="llama3")
llm_with_tools = llm.bind_tools(tools)

def ask(question):
    print(question)
    answer = llm_with_tools.invoke(question)
    return answer.content

# Create your views here.
def search(request, term):
    #answer = ask(term)
    answer = 'Hello'
    return JsonResponse({'answer': answer})

def main(request):
    return render(request, 'index.html')