import aiohttp
from LLM.domain.entities import ChatCompletion, ChatResponse
from LLM.domain.interfaces.repositories import AIProvider

class OllamaProvider(AIProvider):
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def generate_completion(self, request: ChatCompletion) -> ChatResponse:
        async with aiohttp.ClientSession() as session:
            messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
            async with session.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": request.model,
                    "messages": messages,
                    "options": {
                        "temperature": request.temperature
                    }
                }
            ) as response:
                result = await response.json()
                return ChatResponse(
                    content=result["message"]["content"],
                    model=request.model,
                    provider="ollama"
                )