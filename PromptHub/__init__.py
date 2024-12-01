from concurrent import futures
from PromptHub.infrastructure.grpc.server import PromptHubServicer
from PromptHub.infrastructure.grpc import prompthub_pb2_grpc
import grpc
import asyncio
import logging

async def create_server(host: str = "[::]:50052", max_workers: int = 10) -> grpc.Server:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    prompthub_pb2_grpc.add_PromptHubServicer_to_server(PromptHubServicer(), server)
    server.add_insecure_port('[::]:50052')
    return server

async def start_server(server: grpc.aio.Server):
    logging.info("Server starting...")
    server.start()
    logging.info("Server started successfully")
    server.wait_for_termination()

def setup_logging():
    # Configure the logging system
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

def runserver():
    # init logging
    setup_logging()

    async def main():
        server = await create_server()
        await start_server(server)
    
    asyncio.run(main())