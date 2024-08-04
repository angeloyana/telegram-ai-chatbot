from dataclasses import dataclass, field

from google.generativeai import ChatSession


@dataclass
class Chatbot:
    chats: dict[str, ChatSession] = field(default_factory=dict)
    current_chat: str | None = None
