from typing import Iterable, Union

import google.generativeai as genai


class GeminiAgent:
    def __init__(
        self, api_key: str, model_name: str, system_prompt: str = None
    ) -> None:
        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel(model_name)
        self._system_prompt = system_prompt

    def start_chat(self):
        if self._system_prompt:
            # 将系统提示词作为对话历史的第一条消息
            history = [
                {"role": "user", "parts": [self._system_prompt]},
                {"role": "model", "parts": ["我理解了，我会按照你的要求回答。"]},
            ]
            return self._model.start_chat(history=history)
        return self._model.start_chat(history=[])

    def stream_generate(self, model_input: Iterable[Union[str, object]]):
        if self._system_prompt:
            full_input = [self._system_prompt] + list(model_input)
            return self._model.generate_content(
                full_input, stream=True
            )
        return self._model.generate_content(model_input, stream=True)
