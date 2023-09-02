from typing import Dict, Optional

from ai import llm
from utils.logging import log


PROMPT = """You are an assistant that helps me find what I'm looking for from a google search. Try to give me a detailed answer to what I'm looking for. Include any useful urls.

This is what I found by doing a google search:
{google_search}

This is what I'm looking for: {task}."""

_8K_TOKENS = 28_000


def summarize(task: str, google_search: Dict[str, Optional[str]]) -> str:
    google_search_str = ""
    for url, summary in google_search.items():
        if len(google_search_str) < _8K_TOKENS:
            google_search_str += f"Url: {url}\n{summary}\n\n"
        else:
            break
    summary, _ = llm.stream_next(
        [
            {
                "role": "user",
                "content": PROMPT.format(task=task, google_search=google_search_str),
            }
        ],
        model="gpt-4",
    )
    log(summary=summary, skip_stdout=True)
    return summary
