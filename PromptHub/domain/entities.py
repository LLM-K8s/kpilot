from dataclasses import dataclass
from typing import Optional, List

@dataclass
class PromptMessage:
    Role: str
    Content: str

@dataclass
class InfoMessage:
    State: str

@dataclass
class PromptProcessingRequest:
    Mode: str
    Title: str
    Prompt: List[PromptMessage]
    Model: str
    Provider: str
    MaxTokens: Optional[int] = None
    Temperature: Optional[float] = None

@dataclass
class PromptProcessingResponse:
    Result: List[PromptMessage]
    Information: List[InfoMessage]
    Model: str
    Provider: str
    MaxTokens: Optional[int] = None
    Temperature: Optional[float] = None