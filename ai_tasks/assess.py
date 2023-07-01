from ai import llm


PROMPT = """You are an assistant that assesess whether I have found enough information to satisfy my google search.
If I have, you must provide me with a detailed answer to what I'm looking for.

This is what I'm looking for: {task}.

I found this text after doing a google search:
{text}"""


def assess_text(text: str, task: str) -> str:
    message, answer = llm.stream_next(
        [{"role": "user", "content": PROMPT.format(task=task, text=text)}],
        model="gpt-3.5-turbo-16k-0613",
    )
    return message
