#
#  script_generator.py
#
#  Created by Eldar Eliav on 2023/05/11.
#

from chat_gpt_session import ChatGPTSession
from log import log

# TODO - write the output strings to files, destination will be provided from the outside for each file

class ScriptGenerator:
    # init
    def __init__(self):
        self._session = self._prepare_session()

    # api methods
    def generate(
        self,
        channel_name: str,
        topic: str,
        is_verbose_print: bool = False
    ) -> (str, str, str):
        script = self._make_script(topic, channel_name)
        captions = self._make_captions()
        description = self._make_description()
        if is_verbose_print:
            log.info(f"SCRIPT:\n{script}")
            log.info(f"CAPTIONS:\n{captions}")
            log.info(f"DESCRIPTION:\n{description}")
        return (script, captions, description)

    # private methods
    def _prepare_session(self):
        return ChatGPTSession(
            """
You are a professional Youtuber. You know what people like to hear.
You like writing populistic scripts for the average joe to enjoy.
            """
        )

    def _make_script(self, topic: str, channel_name: str) -> str:
        return self._session.ask(
            f"""
Write a youtube video script according to the following specifications:

- Script topic to write on: {topic}
- The Script section must start with: Hey there!! And welcome back. Today! on "{channel_name}", we are going to talk about: <SCRIPT TOPIC HERE>.
- make it sound edgy, spicy and populistic.
- The Script final section will always be: Like and Subscribe for more amazing content on "{channel_name}"
- Acronym words must be with dots between the letters. Example: "AI" -> "A.I", "ASI" -> "A.S.I", etc.
- Write around 10 paragraphs for the script; Each paragraph should have around 100 words; In total you need to reach 500 words.
            """
        )

    def _make_captions(self) -> str:
        return self._session.ask(
            """
Now write the captions section according to the script you wrote, as follows:

- Acording to the script you wrote, write at least 10 captions that will visually describe the script.
- One caption per line (Do NOT start the caption with a prefix of `-` or number, just write the text).
- Each caption will be a simple description of an action, of something/someone doing something, somewhere.
- Each caption text will indicate a random art style, like "Graffiti Art", "Cyber Punk", "Neon Lights", etc.
- Each caption will be used to generate an image using Text To Image.
            """
        )

    def _make_description(self) -> str:
        return self._session.ask(
            """
Now write the description section according to the script you wrote, as follows:

- Write a short desription of 50 words max of what's going on in the `SCRIPT` you wrote.
- Write 5 hashtags describing the main keywords.
            """
        )
