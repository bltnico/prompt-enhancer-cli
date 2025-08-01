import os
from openai import OpenAI
from pydantic import BaseModel
from rich.progress import Progress, SpinnerColumn, TextColumn

from .utils import get_system_prompt, prepare_generator_prompt

client = OpenAI(
    base_url=os.environ.get("LLM_API_BASE_URL", "https://api.openai.com/v1"),
    api_key=os.environ.get("LLM_API_KEY"),
)

CONTEXT_MODEL = os.environ.get("LLM_CONTEXT_MODEL","gpt-4.1-mini-2025-04-14")
GENERATOR_MODEL = os.environ.get("LLM_GENERATOR_MODEL", "gpt-4.1-2025-04-14")

class AskContextSchema(BaseModel):
    questions: list[str]

def ask_context(user_input: str):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Processing...", total=None)

        response = client.responses.parse(
            model=CONTEXT_MODEL,
            instructions=get_system_prompt("context"),
            input=user_input,
            text_format=AskContextSchema,
        )

        context_schema = response.output_parsed
        if not context_schema.questions:
            raise ValueError("No questions generated from the input.")
        return context_schema.questions

def generate_prompt(user_prompt: str, context_list: list[str], keep_user_language: bool) -> str:
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Processing...", total=None)

        response = client.responses.create(
            model=GENERATOR_MODEL,
            input=prepare_generator_prompt(
                system_prompt=get_system_prompt("generator"),
                user_prompt=user_prompt,
                context_list=context_list,
                keep_user_language=keep_user_language
            ),
        )

        return response.output_text

