import json
import re
from typing import Optional

from pydantic import BaseModel, Field

from ai import llm
from utils.io import print_system


class Assessment(BaseModel):
    is_helpful: bool = Field(description="Does it help me satisfy my google search?")
    relevant_text: Optional[str] = Field(
        None, description="Extract the text that contains the information that I need."
    )


FUNCTIONS = [
    {
        "name": "assessment",
        "description": "Make an assessment.",
        "parameters": Assessment.schema(),
    }
]


PROMPT = """You are an assistant that assesess whether I have found information to help me satisfy my google search.
If I have, extract the text that contains the information that I need.

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
    # Not sure. This works.
    arguments = json.dumps(arguments)
    arguments = json.loads(arguments, strict=False)
    return Assessment.parse_raw(arguments)
