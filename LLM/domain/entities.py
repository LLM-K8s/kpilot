from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Message:
    content: str
    role: str

@dataclass
class ChatCompletion:
    model: str
    messages: List[Message]
    provider: str
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None

@dataclass
class ChatResponse:
    content: str
    model: str
    provider: str