from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional

import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from ai_tasks.assess import Assessment, assess_text
from ai_tasks.rephrase import rephrase
from ai_tasks.summarize import summarize
from utils.io import print_system


load_dotenv()


_12K_TOKENS = 48_000


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


def scrape_and_summarize(url: str, task: str) -> Optional[Assessment]:
    print_system(url)
    text = scrape_url(url)
    if len(text) < _12K_TOKENS:
        assessment = assess_text(text, task)
        if assessment.is_helpful:
            return assessment
    return None


def perform_task(task: str, parallel: bool = True) -> None:
    query = rephrase(task)
    print_system(query)
    google_results = google_search(query)

    if parallel:
        with ThreadPoolExecutor(max_workers=2) as executor:
            assesments = list(
                executor.map(
                    scrape_and_summarize, google_results, [task] * len(google_results)
                )
            )
    else:
        # For debugging
        assesments = []
        for url in google_results:
            assesments.append(scrape_and_summarize(url, task))
            breakpoint()

    summaries = {
        url: a.relevant_text for url, a in zip(google_results, assesments) if a
    }

    summarize(task, summaries)
