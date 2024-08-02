from django.shortcuts import render
from django.http import JsonResponse
import requests
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
import requests
from bs4 import BeautifulSoup
import time

def scrape(term):
    boogle = requests.get('https://boogle.boreal.express/search?q=' + term)
    boogl = BeautifulSoup(boogle.content, 'html.parser')
    results = boogl.find_all('a')
    results.pop(0)
    print(results)
    links = []
    titles = []
    for link in boogl.find_all('a'):
        l = link.get('href')
        if l not in links:
            links.append(l)
    links = links[:4]
    for l in links:
        r = requests.get(l)
        soup = BeautifulSoup(r.content, 'html.parser')
        titles.append(soup.title.string)
    t = ''
    for title in titles:
        t += title + ' ' + links[titles.index(title)] + '\n'
    prompt = [(
            "system",
            "You are a helpful assistant. Search the most suited website from the search results."
        ),
        ("user", "Search results: " + t),
        ("user", "Search term: " + term)
    ]
    llm = ChatOllama(model="llama3")
    answer = llm.invoke(question)
    return answer.content

def ask(question):
#    print(question)
#    answer = scrape(question)
#    print(answer)
    if 'ad' in question:
        answer = 'You can check out the boreal ad service.'
    else:
        answer = 'Im happy to help you with searching or scraping websites. What can I do for you?'
    time.sleep(10)
    return answer

# Create your views here
def search(request, term):
    print(term)
    answer = ask(term)
    print(answer)
    return JsonResponse({'answer': answer})

def main(request):
    return render(request, 'index.html')