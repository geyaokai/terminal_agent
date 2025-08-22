import sys

from src.agent import GeminiAgent
from src.config import get_model_name, load_api_key, get_system_prompt
from src.cli import run_interactive_mode, run_one_shot_mode


def main() -> None:
    api_key = load_api_key()
    model_name = get_model_name()
    system_prompt = get_system_prompt()
    agent = GeminiAgent(
        api_key=api_key, model_name=model_name, system_prompt=system_prompt
    )

    if len(sys.argv) == 1:
        run_interactive_mode(agent)
    else:
        run_one_shot_mode(agent)


if __name__ == "__main__":
    main()
