from typing import List

import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from ai_tasks.rephrase import rephrase
from ai_tasks.assess import assess_text
from utils.io import print_system


load_dotenv()


_12K_TOKENS = 30_000


def google_search(query: str) -> List:
    google_key = os.environ.get("GOOGLE_SEARCH_KEY")
    cx = os.environ.get("GOOGLE_CX")
    response = requests.get(
        f"https://customsearch.googleapis.com/customsearch/v1?cx={cx}&q={query}&key={google_key}"
    )
    return [r["link"] for r in response.json()["items"]]


def scrape_url(url: str):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
        text = "\n".join(line for line in text.splitlines() if line.strip())
        return text
    return "Error scraping the website."


def perform_task(task: str) -> str:
    query = rephrase(task)
    print_system(query)
    google_results = google_search(query)
    for url in google_results:
        print_system(url)
        text = scrape_url(url)
        print_system(text)
        if len(text) < _12K_TOKENS:
            assessment = assess_text(text, task)
            breakpoint()
