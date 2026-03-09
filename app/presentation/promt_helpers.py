from prompt_toolkit import prompt, choice


def promt_yes_no(question: str):
    result = choice(message=f"{question}?", options=[
        ("yes", "Yes"),
        ("no", "No")
    ])

    return result == "yes"
