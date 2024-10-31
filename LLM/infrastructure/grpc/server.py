import grpc
from concurrent import futures
import LLM.infrastructure.grpc.ai_service_pb2 as ai_service_pb2
import LLM.infrastructure.grpc.ai_service_pb2_grpc as ai_service_pb2_grpc
from LLM.application.interfaces import AIService
from LLM.domain.entities import ChatCompletion, Message

class AIServiceServer(ai_service_pb2_grpc.AIServiceServicer):
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service

    async def GenerateCompletion(
        self,
        request: ai_service_pb2.ChatCompletionRequest,
        context: grpc.aio.ServicerContext
    ) -> ai_service_pb2.ChatCompletionResponse:
        messages = [
            Message(role=msg.role, content=msg.content)
            for msg in request.messages
        ]

        completion = ChatCompletion(
            model=request.model,
            messages=messages,
            provider=request.provider,
            max_tokens=request.max_tokens if request.HasField('max_tokens') else None,
            temperature=request.temperature if request.HasField('temperature') else None
        )

        response = await self.ai_service.generate_chat_completion(completion)

        return ai_service_pb2.ChatCompletionResponse(
            content=response.content,
            model=response.model,
            provider=response.provider
        )
