import gc
import weakref

from app.ask import ask, interactive_chat


class FakeChat:
    def __init__(self, client_ref=None):
        self.questions = []
        self.client_ref = client_ref

    def send_message(self, question):
        if self.client_ref is not None:
            gc.collect()
            assert self.client_ref() is not None
        self.questions.append(question)

        class Response:
            usage_metadata = None
            text = f"回答: {question}"

        return Response()


def test_interactive_chat_sends_follow_up_questions_to_same_chat(monkeypatch, capsys):
    chat = FakeChat()

    class FakeClient:
        def __init__(self):
            self.chats = self

        def create(self, *, model):
            del model
            return chat

    client = FakeClient()
    questions = iter(["それを詳しく説明して", "/exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(questions))

    interactive_chat(client, "LoRAとは？")

    assert chat.questions == ["LoRAとは？", "それを詳しく説明して"]
    assert "回答: それを詳しく説明して" in capsys.readouterr().out


def test_ask_uses_provided_chat():
    chat = FakeChat()

    answer = ask("続けて質問", chat)

    assert answer == "回答: 続けて質問"
    assert chat.questions == ["続けて質問"]


def test_ask_creates_chat_from_client(monkeypatch):
    class FakeClient:
        def __init__(self, *, api_key):
            del api_key
            self.chat = FakeChat(weakref.ref(self))
            self.chats = self

        def create(self, *, model):
            del model
            return self.chat

    monkeypatch.setattr("app.ask.genai.Client", FakeClient)
    monkeypatch.setattr("app.ask.get_api_key", lambda: "test-key")

    answer = ask("質問")

    assert answer == "回答: 質問"
