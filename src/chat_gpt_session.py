#
#  chat_gpt_session.py
#
#  Created by Eldar Eliav on 2023/05/11.
#

import openai

class ChatGPTSession:
    # private properties
    _chat_session = openai.ChatCompletion()
    _chat_log = []

    # init
    def __init__(self, system_message: str):
        self._set_system_message(system_message)

    # api methods
    def ask(self, question: str) -> str:
        self._chat_log.append({
            'role': 'user',
            'content': question
        })
        response = self._chat_session.create(
            model = 'gpt-3.5-turbo',
            messages = self._chat_log
        )
        answer = response.choices[0]['message']['content']
        self._chat_log.append({
            'role': 'assistant',
            'content': answer
        })
        return answer

    def get_last_answer(self) -> str:
        for entry in self._chat_log[::-1]:
            if entry['role'] == 'user':
                return entry['content']
        return None

    # private methods
    def _set_system_message(self, message: str):
        self._chat_log = [{
            'role': 'system',
            'content': message
        }]
