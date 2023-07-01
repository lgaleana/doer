import json
import re
from typing import Optional

from pydantic import BaseModel, Field

from ai import llm
from utils.io import print_system


class Assessment(BaseModel):
    is_helpful: bool = Field(description="Does it help me satisfy my google search?")
    detailed_answer: Optional[str] = Field(
        None, description="Detailed answer to what I'm looking for."
    )


FUNCTIONS = [
    {
        "name": "assessment",
        "description": "Make an assessment.",
        "parameters": Assessment.schema(),
    }
]


PROMPT = """You are an assistant that assesess whether I have found information to help me satisfy my google search.
If I have, you must provide me with a detailed answer to what I'm looking for.

I found this text after doing a google search:
{text}

This is what I'm looking for: {task}."""


def assess_text(text: str, task: str) -> Assessment:
    _, assessment = llm.stream_next(
        [{"role": "user", "content": PROMPT.format(task=task, text=text)}],
        model="gpt-3.5-turbo-16k-0613",
        functions=FUNCTIONS,
        function_call={"name": "assessment"},  # type: ignore
    )
    print_system(assessment["arguments"])
    return _parse_response(assessment["arguments"])


def _parse_response(arguments: str) -> Assessment:
    # For parsing text with code.
    match = re.search('"""(.*)"""', arguments, re.DOTALL)
    if match:
        escaped = json.dumps(match.group(1))
        arguments = re.sub('(""".*""")', f"{escaped}", arguments, flags=re.DOTALL)
    arguments = json.loads(arguments, strict=False)
    return Assessment.model_validate(arguments)
