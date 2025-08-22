import io
import os
import platform
import subprocess
from typing import Optional, Tuple, Union

from PIL import Image

if platform.system() == "Windows":
    from PIL import ImageGrab


IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"]
TEXT_EXTENSIONS = [
    ".txt",
    ".py",
    ".js",
    ".html",
    ".css",
    ".md",
    ".json",
    ".xml",
    ".c",
    ".cpp",
    ".java",
    ".go",
    ".rs",
    ".sh",
]


def process_file_input(
    file_path: str,
) -> Tuple[Optional[Union[Image.Image, str]], Optional[str]]:
    """Process file input by extension.

    - Images -> return PIL Image
    - Text -> return formatted string
    Returns (content, error_message)
    """
    try:
        clean_path = file_path.strip().strip("'\"")
        _, extension = os.path.splitext(clean_path)

        if not os.path.exists(clean_path):
            return None, f"错误：找不到文件 '{clean_path}'"

        if extension.lower() in IMAGE_EXTENSIONS:
            image = Image.open(clean_path)
            return image, None

        if extension.lower() in TEXT_EXTENSIONS:
            with open(clean_path, "r", encoding="utf-8") as f:
                content = f.read()
            formatted_text = f"以下是文件 '{os.path.basename(clean_path)}' 的内容:\n\n---\n\n{content}\n\n---"
            return formatted_text, None

        return None, f"错误：不支持的文件类型 '{extension}'。目前支持图片和文本文件。"

    except FileNotFoundError:
        return None, f"错误：找不到文件 '{file_path}'"
    except Exception as e:  # noqa: BLE001
        return None, f"处理文件时出错: {e}"


def read_clipboard_image():
    """Read image from system clipboard if supported.

    Returns PIL Image or raises exceptions on failure.
    """
    current_os = platform.system()

    if current_os == "Linux":
        command = [
            "xclip",
            "-selection",
            "clipboard",
            "-t",
            "image/png",
            "-o",
        ]
        result = subprocess.run(command, capture_output=True, check=True, timeout=5)
        image_data = result.stdout
        if not image_data:
            raise RuntimeError("错误：剪贴板中没有图片，或者图片格式不是PNG。")
        return Image.open(io.BytesIO(image_data))

    if current_os == "Windows":
        content = ImageGrab.grabclipboard()
        if content is None:
            raise RuntimeError("错误：剪贴板中没有图片。")
        return content

    raise RuntimeError(f"错误：剪贴板功能暂不支持当前操作系统 ({current_os})。")
