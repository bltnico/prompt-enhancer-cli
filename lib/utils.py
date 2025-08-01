import os
import questionary

def select_prompt_output_format() -> str:
    label = "Select the output format:"
    choices = ["Auto", "Markdown", "Spreadsheets", "Reports", "Presentations"]
    choice = questionary.select(label, choices=choices).ask()
    return "%s %s" % (label, choice)

def get_system_prompt(prompt_file: str) -> str:
    base_dir = os.path.dirname(__file__)
    path = os.path.join(base_dir, "prompts", f"{prompt_file}.txt")
    with open(path, encoding="utf-8") as p:
        return p.read()

def prepare_generator_prompt(
        system_prompt: str,
        user_prompt: str,
        context_list: list[str],
        keep_user_language: bool,
    ) -> str:
    context_str = "\n".join(context_list)
    prompt_language = "Write in **the same language as the ORIGINAL REQUEST**." if keep_user_language else "Write in **English.**"
    system_prompt = system_prompt.replace("<<ORIGINAL_REQUEST>>", user_prompt)
    system_prompt = system_prompt.replace("<<Q_AND_A_BLOCK>>", context_str)
    system_prompt = system_prompt.replace("<<PROMPT_LANGUAGE>>", prompt_language)
    return system_prompt
