from openai import AsyncOpenAI
from LLM.domain.entities import ChatCompletion, ChatResponse
from LLM.domain.interfaces.repositories import AIProvider

class OpenAIProvider(AIProvider):
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)

    async def generate_completion(self, request: ChatCompletion) -> ChatResponse:
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        response = await self.client.chat.completions.create(
            model=request.model,
            messages=messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        return ChatResponse(
            content=response.choices[0].message.content,
            model=request.model,
            provider="openai"
        )