from typing import Dict, Optional

from ai import llm


PROMPT = """You are an assistant that helps me find what I'm looking for from a google search. Try to give me a detailed answer to what I'm looking for. Include any useful urls.

This is what I found by doing a google search:
{google_search}

This is what I'm looking for: {task}."""


def summarize(task: str, google_search: Dict[str, Optional[str]]) -> str:
    google_search_str = "\n\n".join(
        f"Url: {url}\n{summary}" for url, summary in google_search.items()
    )
    summary, _ = llm.stream_next(
        [
            {
                "role": "user",
                "content": PROMPT.format(task=task, google_search=google_search_str),
            }
        ],
    )
    return summary
