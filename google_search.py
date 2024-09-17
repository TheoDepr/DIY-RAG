from bs4 import BeautifulSoup
from googlesearch import search
import requests


def google_query(query, n=10, lang="en", region="uk"):
    search_results = []
    for url in search(query, num_results=n, lang=lang, region=region):
        search_results.append(url)
    return search_results


def scrape_url(query):
    response = requests.get(query)
    soup = BeautifulSoup(response.text, 'html.parser')
    first_result = soup.get_text()
    return first_result


# Example usage:
if __name__ == "__main__":
    content = scrape_url("")
    print(content)
