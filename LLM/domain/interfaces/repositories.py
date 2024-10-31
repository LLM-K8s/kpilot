from abc import ABC, abstractmethod
from LLM.domain.entities import ChatCompletion, ChatResponse

class AIProvider(ABC):
    @abstractmethod
    async def generate_completion(self, request: ChatCompletion) -> ChatResponse:
        pass