import argparse
import re
import sys
from typing import List

from .utils import process_file_input, read_clipboard_image


def run_one_shot_mode(agent) -> None:
    parser = argparse.ArgumentParser(description="多模态终端 Agent (单次执行模式)")
    parser.add_argument("prompt", type=str, nargs="?", default="", help="你的文本问题")
    parser.add_argument("-i", "--input", type=str, help="输入文件的路径 (图片或文本)")

    args = parser.parse_args(sys.argv[1:])

    if not sys.stdin.isatty() and not args.prompt:
        stdin_text = sys.stdin.read().strip()
        if stdin_text:
            args.prompt = stdin_text

    prompt = args.prompt
    file_path = args.input

    if not prompt and not file_path:
        print("请输入问题或提供一个文件。")
        parser.print_help()
        sys.exit(1)

    model_input: List[object] = []

    if file_path:
        content, error = process_file_input(file_path)
        if error:
            print(error)
            sys.exit(1)
        model_input.append(content)

    if prompt:
        model_input.append(prompt)

    response = agent.stream_generate(model_input)
    for chunk in response:
        print(chunk.text, end="", flush=True)
    print()


def run_interactive_mode(agent) -> None:
    print("您好！我是您的Shell专家")
    print("输入 'exit'、'quit'、Ctrl+C 或 Ctrl+D 退出。")
    print("使用 -i <文件路径> 来载入图片或代码文件 (支持拖拽文件到终端)。")
    chat = agent.start_chat()

    while True:
        try:
            user_input = input(">> ")

            if user_input.lower() in ["exit", "quit"]:
                print("再见！")
                break

            model_input: List[object] = []
            prompt = user_input

            match = re.search(r"(-i|--input)\s+(.*)", user_input, re.DOTALL)
            if match:
                file_path_str = match.group(2).strip()
                prompt = user_input.replace(match.group(0), "").strip()

                if file_path_str.lower() in ["clipboard", "paste", "p"]:
                    try:
                        file_content = read_clipboard_image()
                        model_input.append(file_content)
                    except Exception as e:  # noqa: BLE001
                        print(str(e))
                        continue
                else:
                    content, error = process_file_input(file_path_str)
                    if error:
                        print(error)
                        continue
                    model_input.append(content)

            if prompt:
                model_input.append(prompt)

            if not model_input:
                continue

            response = chat.send_message(model_input, stream=True)
            for chunk in response:
                print(chunk.text, end="", flush=True)
            print()

        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break
        except Exception as e:  # noqa: BLE001
            print(f"\n发生错误: {e}")
            break
