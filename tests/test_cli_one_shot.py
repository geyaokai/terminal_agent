import sys
from types import SimpleNamespace

import pytest

from src.cli import run_one_shot_mode


class FakeChunk:
    def __init__(self, text: str) -> None:
        self.text = text


class FakeAgent:
    def __init__(self) -> None:
        self.inputs = None

    def stream_generate(self, model_input):
        self.inputs = list(model_input)
        return [FakeChunk("OK")]  # emulate streamed chunks


def test_cli_one_shot_with_prompt(monkeypatch, capsys):
    fake = FakeAgent()
    monkeypatch.setattr(sys, "argv", ["prog", "hello"])
    run_one_shot_mode(fake)
    captured = capsys.readouterr()
    assert "OK" in captured.out
    assert fake.inputs[-1] == "hello"


def test_cli_one_shot_with_stdin(monkeypatch, capsys):
    fake = FakeAgent()

    class FakeIn:
        def __init__(self, s: str) -> None:
            self._s = s

        def read(self):
            return self._s

        def isatty(self):
            return False

    monkeypatch.setattr(sys, "argv", ["prog"])  # no args
    monkeypatch.setattr(sys, "stdin", FakeIn("from stdin"))
    run_one_shot_mode(fake)
    captured = capsys.readouterr()
    assert "OK" in captured.out
    assert fake.inputs[-1] == "from stdin"
