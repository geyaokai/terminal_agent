import os
from pathlib import Path

import pytest

from src.utils import process_file_input


def write_temp_file(tmp_path: Path, name: str, content: str) -> str:
    p = tmp_path / name
    p.write_text(content, encoding="utf-8")
    return str(p)


def test_process_file_input_text_file(tmp_path: Path):
    path = write_temp_file(tmp_path, "sample.txt", "hello world")
    content, error = process_file_input(path)
    assert error is None
    assert isinstance(content, str)
    assert "hello world" in content


def test_process_file_input_missing_file():
    content, error = process_file_input("/nonexistent/file.txt")
    assert content is None
    assert "找不到文件" in error


def test_process_file_input_unsupported_extension(tmp_path: Path):
    path = write_temp_file(tmp_path, "data.bin", "binary? not really")
    content, error = process_file_input(path)
    assert content is None
    assert "不支持的文件类型" in error


def test_process_file_input_strips_quotes(tmp_path: Path):
    path = write_temp_file(tmp_path, "code.py", "print('ok')")
    quoted = f"'{path}'"
    content, error = process_file_input(quoted)
    assert error is None
    assert isinstance(content, str)
    assert "print('ok')" in content
