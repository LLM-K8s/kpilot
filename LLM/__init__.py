import asyncio
import grpc
from concurrent import futures
import os
from typing import Dict
import signal
import logging

from LLM.infrastructure.grpc.server import AIServiceServer
from LLM.infrastructure.ai_providers.openai_provider import OpenAIProvider
from LLM.infrastructure.ai_providers.ollama_provider import OllamaProvider
from LLM.infrastructure.grpc import ai_service_pb2_grpc
from LLM.application.services import AIGatewayService


async def create_server(
    providers: Dict[str, str],
    host: str = "[::]:50051",
    max_workers: int = 10
) -> grpc.aio.Server:
    """
    Create and configure the gRPC server

    Args:
        providers: Dictionary of provider configurations
                  e.g. {"openai": "api-key", "ollama": "http://localhost:11434"}
        host: Host address for the server
        max_workers: Maximum number of worker threads
    """
    ai_providers = {
        "openai": OpenAIProvider(api_key=providers["openai"]),
        "ollama": OllamaProvider(base_url=providers["ollama"])
    }

    ai_service = AIGatewayService(ai_providers)
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    ai_service_pb2_grpc.add_AIServiceServicer_to_server(
        AIServiceServer(ai_service),
        server
    )

    server.add_insecure_port(host)
    return server

async def serve(server: grpc.aio.Server):
    """Start and run the server"""
    loop = asyncio.get_running_loop()

    async def shutdown(sig, loop):
        logging.info(f"Received signal {sig.name}...")
        logging.info("Shutting down server...")
        await server.stop(grace=5)
        loop.stop()

    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(
            sig,
            lambda s=sig: asyncio.create_task(shutdown(s, loop))
        )

    logging.info("Server starting...")
    await server.start()
    logging.info("Server started successfully")
    await server.wait_for_termination()

def setup_logging():
    """Configure the logging system"""
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'

    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(),  # output to console
            # logging.FileHandler('server.log')  # save to file
        ]
    )

def load_provider_config() -> Dict[str, str]:
    """Load vendor configuration from environment variables"""
    return {
        "openai": os.getenv("OPENAI_API_KEY", "your-openai-api-key"),
        "ollama": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    }

def run():
    """Main entry point for running the server"""
    # Initialize the log system
    setup_logging()

    # Load configuration
    providers = load_provider_config()

    logging.info("Starting server with configuration:")
    logging.info(f"OpenAI API endpoint configured: {'yes' if providers['openai'] != 'your-openai-api-key' else 'no'}")
    logging.info(f"Ollama endpoint: {providers['ollama']}")

    # Create and run server
    async def main():
        server = await create_server(providers)
        await serve(server)

    asyncio.run(main())
