import typer
import pyperclip
from rich import print

from dotenv import load_dotenv
load_dotenv()

from lib import llm
from lib.utils import select_prompt_output_format

app = typer.Typer()

@app.command()
def cli(clipboard: bool = True):
    context: list[str] = []
    user_prompt = typer.prompt("What's your prompt?")
    if not user_prompt:
        raise typer.Exit("No prompt provided")

    typer.echo("Asking context questions...\n")
    llm_questions = llm.ask_context(user_prompt)
    for question in llm_questions:
        answer = typer.prompt(question)
        context.append("%s %s" % (question, answer))

    context.append(select_prompt_output_format())

    typer.echo("\nGenerating prompt...")
    final_prompt = llm.generate_prompt(user_prompt, context)
    typer.echo("Generated prompt:\n")
    typer.echo(final_prompt)

    if clipboard:
        pyperclip.copy(final_prompt)
        print("\n[bold]Prompt copied to clipboard[/bold]")

if __name__ == "__main__":
    app()
