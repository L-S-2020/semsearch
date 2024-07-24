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

if __name__ == '__main__':
    term = input('Enter a term: ')
    scrape(term)