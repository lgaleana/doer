from typing import List

from googlesearch import search

def google_search(query: str) -> List:
    return list(search(query))