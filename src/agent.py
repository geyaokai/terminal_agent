from typing import Iterable, Union

import google.generativeai as genai


class GeminiAgent:
    def __init__(self, api_key: str, model_name: str) -> None:
        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel(model_name)

    def start_chat(self):
        return self._model.start_chat(history=[])

    def stream_generate(self, model_input: Iterable[Union[str, object]]):
        return self._model.generate_content(model_input, stream=True)
