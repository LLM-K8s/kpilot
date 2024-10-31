from abc import ABC, abstractmethod
from LLM.domain.entities import ChatCompletion, ChatResponse

class AIService(ABC):
    @abstractmethod
    async def generate_chat_completion(self, request: ChatCompletion) -> ChatResponse:
        pass