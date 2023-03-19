import os
import openai


def get_room_description():
    # TODO: keep working on this
    openai.api_key = os.getenv("OPENAI_API_KEY")
    r = openai.Completion.create(
        model="text-davinci-003",
        prompt="Generate an interesting description for a room in a maze.",
        max_tokens=15,
        temperature=0.8,
    )
    return r.choices[0].text


print(get_room_description())
