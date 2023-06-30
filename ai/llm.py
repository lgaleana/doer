import os
from typing import Any, Dict, List, Optional, Tuple

import openai
from dotenv import load_dotenv

from utils.io import print_assistant

load_dotenv()


openai.api_key = os.environ["OPENAI_KEY_PERSONAL"]
MODEL = "gpt-3.5-turbo-0613"
TEMPERATURE = 0.0


def call(
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    stop: Optional[str] = None,
    stream: Optional[bool] = None,
    functions: Optional[List] = None,
    function_call="auto",
) -> Dict[str, Any]:
    if not model:
        model = MODEL
    if temperature is None:
        temperature = TEMPERATURE

    if functions is not None:
        return openai.ChatCompletion.create(  # type: ignore
            model=model,
            messages=messages,
            temperature=temperature,
            stop=stop,
            stream=stream,
            functions=functions,
            function_call=function_call,
        )
    return openai.ChatCompletion.create(  # type: ignore
        model=model,
        messages=messages,
        temperature=temperature,
        stop=stop,
        stream=stream,
    )


def next(
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    stop: Optional[str] = None,
) -> str:
    return call(messages, model, temperature, stop, stream=False)["choices"][0][
        "message"
    ]["content"]


def stream_next(
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    stop: Optional[str] = None,
    functions: Optional[List] = None,
    function_call="auto",
) -> Tuple[Optional[str], Optional[Dict]]:
    response = call(
        messages,
        model,
        temperature,
        stop,
        stream=True,
        functions=functions,
        function_call=function_call,
    )

    message = None
    function_ = None
    for chunk in response:
        delta = chunk["choices"][0]["delta"]
        if "content" in delta and delta["content"]:
            message = stream(delta, message)
        elif "function_call" in delta and delta["function_call"]:
            function_ = collect_function(delta, function_)
    print_assistant()
    return message, function_


def stream(delta: Dict[str, str], message: Optional[str]) -> str:
    if message is None:
        message = ""
    message += delta["content"]
    print_assistant(delta["content"], end="", flush=True)
    return message


def collect_function(delta: Dict, function_) -> Dict:
    if function_ is None:
        function_ = {}
    func_call = delta["function_call"]
    for k in func_call:
        if k not in function_:
            function_[k] = func_call[k]
        else:
            function_[k] += func_call[k]
    print_assistant(".", end="", flush=True)
    return function_
