from ai import llm


PROMPT = """Convert what I'm looking for into a proper google search. No quotes.

What I'm looking for: {task}.

notalk;justgo"""


def rephrase(task: str) -> str:
    return llm.next([{"role": "user", "content": PROMPT.format(task=task)}])
