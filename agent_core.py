# agent_core.py

import os
import sys
import argparse
import re
import subprocess
import io
import readline  # <-- 增强 input() 功能，支持方向键和历史记录
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

# --- 新增：定义支持的文件类型 ---
IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.webp', '.bmp', '.gif']
TEXT_EXTENSIONS = ['.txt', '.py', '.js', '.html', '.css', '.md', '.json', '.xml', '.c', '.cpp', '.java', '.go', '.rs', '.sh']

def process_file_input(file_path):
    """
    根据文件扩展名，智能处理文件输入。
    - 如果是图片，返回Pillow Image对象。
    - 如果是文本，读取内容并格式化后返回字符串。
    - 如果失败或不支持，返回None和错误信息。
    """
    try:
        # 修复路径解析问题：去除可能存在的多余引号和空格
        clean_path = file_path.strip().strip("'\"")
        
        # 获取文件扩展名
        _, extension = os.path.splitext(clean_path)
        
        if not os.path.exists(clean_path):
            return None, f"错误：找不到文件 '{clean_path}'"

        if extension.lower() in IMAGE_EXTENSIONS:
            image = Image.open(clean_path)
            return image, None
        
        elif extension.lower() in TEXT_EXTENSIONS:
            with open(clean_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 格式化文本输出，让模型更好地理解上下文
            formatted_text = f"以下是文件 '{os.path.basename(clean_path)}' 的内容:\n\n---\n\n{content}\n\n---"
            return formatted_text, None
        
        else:
            return None, f"错误：不支持的文件类型 '{extension}'。目前支持图片和文本文件。"

    except FileNotFoundError:
        return None, f"错误：找不到文件 '{file_path}'"
    except Exception as e:
        return None, f"处理文件时出错: {e}"


def run_one_shot_mode(model):
    """处理单次执行的命令"""
    parser = argparse.ArgumentParser(description="多模态终端 Agent (单次执行模式)")
    parser.add_argument("prompt", type=str, nargs='?', default="", help="你的文本问题")
    # 将 -i/--image 改为更通用的 -i/--input
    parser.add_argument("-i", "--input", type=str, help="输入文件的路径 (图片或文本)")
    
    if len(sys.argv) == 2 and not sys.stdin.isatty():
        args = parser.parse_args([sys.stdin.read().strip()])
    else:
        args = parser.parse_args(sys.argv[2:])

    prompt = args.prompt
    file_path = args.input
    
    if not prompt and not file_path:
        print("请输入问题或提供一个文件。")
        parser.print_help()
        sys.exit(1)

    model_input = []
    
    if file_path:
        file_content, error = process_file_input(file_path)
        if error:
            print(error)
            sys.exit(1)
        model_input.append(file_content)
            
    if prompt:
        model_input.append(prompt)

    generate_and_print_response(model, model_input)


def run_interactive_mode(model):
    """启动交互式聊天模式"""
    print("已进入交互式对话模式。输入 'exit'、'quit'、Ctrl+C 或 Ctrl+D 退出。")
    print("使用 -i <文件路径> 来载入图片或代码文件 (支持拖拽文件到终端)。")
    chat = model.start_chat(history=[])
    
    while True:
        try:
            user_input = input(">> ")

            if user_input.lower() in ["exit", "quit"]:
                print("再见！")
                break
            
            model_input = []
            prompt = user_input
            
            # 使用更健壮的方式来解析文件路径
            match = re.search(r'(-i|--input)\s+(.*)', user_input, re.DOTALL)
            if match:
                file_path_str = match.group(2).strip()
                # 从原始输入中移除文件路径部分，剩下的就是prompt
                prompt = user_input.replace(match.group(0), "").strip()

                if file_path_str.lower() in ["clipboard", "paste"]:
                    # (剪贴板功能暂时只保留对图片的支持，未来可以扩展)
                    try:
                        command = ["xclip", "-selection", "clipboard", "-t", "image/png", "-o"]
                        result = subprocess.run(command, capture_output=True, check=True, timeout=5)
                        image_data = result.stdout
                        
                        if not image_data:
                            print("错误：剪贴板中没有图片，或者图片格式不是PNG。")
                            continue

                        file_content = Image.open(io.BytesIO(image_data))
                        model_input.append(file_content)

                    except FileNotFoundError:
                        print("错误：命令 'xclip' 未找到。请先运行 'sudo apt-get install xclip'。")
                        continue
                    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                        print("错误：无法从剪贴板获取图片。请确认剪贴板中有一张图片。")
                        continue
                else:
                    # 使用新的文件处理函数
                    file_content, error = process_file_input(file_path_str)
                    if error:
                        print(error)
                        continue
                    model_input.append(file_content)

            # 确保prompt不为空时才加入
            if prompt:
                model_input.append(prompt)
            
            # 如果没有任何有效输入，则跳过
            if not model_input:
                continue

            response = chat.send_message(model_input, stream=True)
            
            for chunk in response:
                print(chunk.text, end="", flush=True)
            print()

        except EOFError:
            print("\n再见！")
            break
        except KeyboardInterrupt:
            print("\n再见！")
            break
        except Exception as e:
            print(f"\n发生错误: {e}")
            break

def generate_and_print_response(model, model_input):
    """通用函数，用于调用API并流式打印结果"""
    try:
        print("🤔 思考中...", file=sys.stderr)
        response = model.generate_content(model_input, stream=True)
        
        for chunk in response:
            print(chunk.text, end='', flush=True)
        print()
        # 重置标准错误输出的颜色
        print("\033[0m", end="", file=sys.stderr)
            
    except Exception as e:
        print(f"\n调用 API 时出错: {e}")
        #sys.exit(1) # 在交互模式中，我们不希望因为一次API错误就退出程序

def main():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("错误：请在 .env 文件中设置 GOOGLE_API_KEY。")
        sys.exit(1)
        
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-2.5-flash')

    if len(sys.argv) == 1:
        run_interactive_mode(model)
    else:
        run_one_shot_mode(model)


if __name__ == "__main__":
    main()