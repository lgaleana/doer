from ai import llm


PROMPT = """I want to know about: {task}.

How would you phrase it as a google search? No quotes."""


def rephrase(task: str) -> str:
    return llm.next([{"role": "user", "content": PROMPT.format(task=task)}], model="gpt-4")
