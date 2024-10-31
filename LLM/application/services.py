from typing import Dict
from LLM.domain.interfaces.repositories import AIProvider
from LLM.domain.entities import ChatCompletion, ChatResponse
from LLM.application.interfaces import AIService

class AIGatewayService(AIService):
    def __init__(self, providers: Dict[str, AIProvider]):
        self.providers = providers

    async def generate_chat_completion(self, request: ChatCompletion) -> ChatResponse:
        provider = self.providers.get(request.provider)
        if not provider:
            raise ValueError(f"Provider {request.provider} not found")
        return await provider.generate_completion(request)
