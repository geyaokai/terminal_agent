@echo off

rem --- 重要：请修改为你的 Windows 绝对路径 ---
set "AGENT_DIR=D:\VScode_workspace\terminal_agent"

rem --- 核心修正：先将工作目录切换到 Agent 的项目目录 ---
rem cd /d 命令可以确保跨驱动器（从 C: 切换到 D:）也能成功
cd /d %AGENT_DIR%

rem --- 现在，uv run 会在正确的项目目录中执行，从而找到 .venv ---
uv run --python 3.10 python agent_core.py %*