# terminal_agent
简单的终端多模态 Agent（文本 + 图片）。支持：
- 文本对话
- 读取图片/文本文件作为上下文
- 从剪贴板读取图片（Windows、Linux）

## 环境配置

### 1) 准备 Python 与依赖
- Python 3.10+
- 建议使用 `uv` 管理虚拟环境与运行：
  - 安装 `uv`（参考官方文档）
  - 在项目根目录执行：
    - 创建/使用虚拟环境（可选）：`uv venv`
    - 安装依赖：`uv pip install -r requirements.txt`

也可以用原生 `venv`：
- `python -m venv .venv`
- Windows 激活：`.\.venv\Scripts\activate`
- Linux 激活：`source .venv/bin/activate`
- `pip install -r requirements.txt`

### 2) 配置 API Key
在项目根目录创建 `.env` 文件，写入：
```
GOOGLE_API_KEY=你的_Gemini_API_Key
```

### 3) 剪贴板依赖（可选）
- Windows：内置的 `PIL.ImageGrab` 即可。
- Linux：若需从剪贴板读取图片，请安装 `xclip`：
  - Debian/Ubuntu: `sudo apt-get install xclip`

## 快速开始

### 方式A：通过 `ag`/`ag.bat` 启动（推荐）
- Windows:
  1. 编辑 `ag.bat`，将 `AGENT_DIR` 改为你的本地项目路径。
  2. 在项目根目录执行：
     - 直接对话：`ag`
     - 一次性问答：`ag "帮我解释这段代码"`
     - 带文件输入：`ag "描述这张图片" -i D:\path\img.png`
     - 从剪贴板取图（Windows 支持）：`ag -i clipboard`
- Linux:
  1. 编辑 `ag`（bash 脚本），将 `AGENT_DIR` 改为你的本地项目路径。
  2. `chmod +x ag`
  3. 在项目根目录执行：
     - 直接对话：`./ag`
     - 一次性问答：`./ag "帮我解释这段代码"`
     - 带文件输入：`./ag "描述这张图片" -i /path/img.png`
     - 从剪贴板取图（需 `xclip`）：`./ag -i clipboard`

提示：
- 可将项目目录加入 PATH，这样可直接在任意目录使用 `ag`。

### 方式B：直接运行 Python 脚本
- 交互模式（无参数启动）：
  ```
  python agent_core.py
  ```
- 单次模式（带问题与输入文件）：
  ```
  python agent_core.py "描述这张图片" -i "D:\path\img.png"
  python agent_core.py "分析这段代码" -i "D:\code\app.py"
  ```
- 管道输入作为问题：
  ```
  type note.txt | python agent_core.py
  ```

## 使用说明

- 进入交互对话后，直接输入问题，或附加文件参数：
  - 文本 + 文件：`我的问题 -i D:\path\file.py`
  - 仅从剪贴板取图：
    - Windows：`-i clipboard` 或 `-i paste`
    - Linux：`-i clipboard`（需 `xclip` 且剪贴板为 PNG 图）
- 支持的文件扩展名：
  - 图片：`.png .jpg .jpeg .webp .bmp .gif`
  - 文本/代码：`.txt .py .js .html .css .md .json .xml .c .cpp .java .go .rs .sh`

## 常见问题

- “错误：请在 .env 文件中设置 GOOGLE_API_KEY。”
  - 未配置或未加载 API Key，请创建 `.env` 并填入 `GOOGLE_API_KEY`。
- Linux 剪贴板取图失败：
  - 安装 `xclip`，并确保剪贴板中是 PNG 图片。
- macOS 剪贴板：
  - 目前未实现从剪贴板读取图片功能，可改用文件路径方式 `-i <图片路径>`。

## 文件与入口
- 代码入口：`agent_core.py`
- 启动脚本：
  - Linux：`ag`（bash）
  - Windows：`ag.bat`

```
