"""第1回: 素のLLMに質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする
    uv run python -m app.ask --interactive "LoRAとは何ですか？"

通常モードは1回だけ質問する。--interactive では会話履歴を保ったまま続けて質問できる。
ツールは使わない「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def new_client() -> genai.Client:
    return genai.Client(api_key=get_api_key())


def ask(question: str, chat: genai.chats.Chat | None = None) -> str:
    if chat is None:
        client = new_client()
        chat = client.chats.create(model=MODEL)
    response = chat.send_message(question)

    # TODO(第1回 演習): response.usage_metadata から
    #   入力トークン数と出力トークン数を表示してみよう（Copilotに頼んでよい）
    if response.usage_metadata is not None:
        print(f"[トークン数] 入力: {response.usage_metadata.prompt_token_count}")
        print(f"[トークン数] 出力: {response.usage_metadata.candidates_token_count}")

    return response.text


def interactive_chat(client: genai.Client, first_question: str) -> None:
    chat = client.chats.create(model=MODEL)
    print("終了するには /exit を入力してください。")
    question = first_question
    while True:
        print(f"\n[質問] {question}\n")
        print(ask(question, chat))
        try:
            question = input("\n次の質問> ").strip()
        except EOFError:
            print()
            return
        if question == "/exit":
            return
        if not question:
            continue


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?")
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="会話履歴を保ったまま続けて質問する",
    )
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    try:
        if args.interactive:
            interactive_chat(new_client(), args.question or DEFAULT_QUESTION)
        else:
            question = args.question or DEFAULT_QUESTION
            print(f"[質問] {question}\n")
            print(ask(question))
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
