from typing import Protocol

from langchain_ollama import ChatOllama


class ChatModel(Protocol):
    def generate(self, prompt: str) -> str:
        raise NotImplementedError

    def stream(self, prompt: str):
        raise NotImplementedError


class OllamaChatModel:
    def __init__(self, *, model: str, base_url: str) -> None:
        self.model = ChatOllama(model=model, base_url=base_url)

    def generate(self, prompt: str) -> str:
        response = self.model.invoke(prompt)
        return str(response.content)

    def stream(self, prompt: str):
        for chunk in self.model.stream(prompt):
            content = getattr(chunk, "content", "")
            if content:
                yield str(content)
