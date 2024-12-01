from concurrent import futures
from PromptHub.infrastructure.grpc import prompthub_pb2
from PromptHub.infrastructure.grpc import prompthub_pb2_grpc
from LLM.infrastructure.grpc import ai_service_pb2
from LLM.infrastructure.grpc import ai_service_pb2_grpc
import grpc
import json
import logging

class PromptHubServicer(prompthub_pb2_grpc.PromptHubServicer):
    def __init__(self):
        self.Jsonfile = "./prompthub/infrastructure/data/repository.json"
        self.AllPrompts = {}
        self.OpenFile()

    def OpenFile(self):
        with open(self.Jsonfile, encoding="utf-8") as f:
            Content = f.read()
            self.AllPrompts = json.loads(Content)

    def SaveFile(self):
        with open(self.Jsonfile, "w", encoding="utf-8") as f:
            json.dump(self.AllPrompts, f, indent=4, ensure_ascii = False)

    def Add(self, Title: str, Prompt: list) -> dict:
        self.OpenFile()
        if Title not in self.AllPrompts.keys():
            self.AllPrompts[Title] = Prompt
            self.SaveFile()
            logging.info(f"Add {Title} successfully.")
            State = f"Add {Title} successfully"
        else:
            logging.error(f"{Title} is already exist.")
            State = f"{Title} is already exist."
        return {
            "State": State,
            "Title": Title
        }

    def Delete(self, Title: str) -> dict:
        self.OpenFile()
        if Title in self.AllPrompts.keys():
            del self.AllPrompts[Title]
            self.SaveFile()
            logging.info(f"Delete {Title} successfully.")
            State = f"Delete {Title} successfully"
        else:
            logging.error(f"{Title} is not exist.")
            State = f"{Title} is not exist."
        return {
            "State": State,
            "Title": Title
        }
    
    def Update(self, Title: str, Prompt: list) -> dict:
        self.OpenFile()
        if Title in self.AllPrompts.keys():
            self.AllPrompts[Title] = Prompt
            logging.info(f"Update {Title} successfully.")
            State = f"Update {Title} successfully."
            self.SaveFile()
        else:
            logging.error(f"{Title} is not exist.")
            State = f"{Title} is not exist."
        return {
            "State": State
        }
    
    def ShowAll(self) -> dict:
        self.OpenFile()
        Text = ""
        for Title in self.AllPrompts.keys():
            Text += f"\n{Title}：\n\tRole：{self.AllPrompts[Title][0]}\n\tContent：{self.AllPrompts[Title][1]}\n"
        logging.info(Text)
        return {
            "State": Text,
        }
    
    def Output(self, Title: str=None, Prompt: list=[]) -> dict:
        Role = ""
        Content = ""
        if Title in self.AllPrompts.keys():
            self.OpenFile()
            logging.info(f"Output {Title}")
            Role = self.AllPrompts[Title][0]
            Content = self.AllPrompts[Title][1]
        elif Prompt != []:
            logging.info(f"Output {Prompt}")
            Role = Prompt[Title][0]
            Content = Prompt[Title][1]
        return {
            "Role": Role,
            "Content": Content
        }

    def PromptProcessing(self,
        Request: prompthub_pb2.PromptProcessingRequest,
        Context: grpc.aio.ServicerContext
    ):
        if Request.Prompt:
            for msg in Request.Prompt:
                Prompt = [msg.Role, msg.Content]
                print(Prompt)
        if Request.Mode.lower() == "add":
            Content = self.Add(Request.Title, Prompt)
        if Request.Mode.lower() == "delete":
            Content = self.Delete(Request.Title)
        if Request.Mode.lower() == "update":
            Content = self.Update(Request.Title, Prompt)
        if Request.Mode.lower() == "showall":
            Content = self.ShowAll()
        if Request.Mode.lower() != "output":
            return prompthub_pb2.PromptProcessingResponse(
                Information = prompthub_pb2.InfoMessage(
                    State = Content["State"]
                )
            )
        else:
            Channel = grpc.insecure_channel("localhost:50051")
            Client = ai_service_pb2_grpc.AIServiceStub(Channel)
            Content = self.Output(Request.Title, Request.Prompt)
            Messages = [
                ai_service_pb2.Message(
                    role = Content["Role"],
                    content = Content["Content"]
                )
            ]
            Generation = ai_service_pb2.ChatCompletionRequest(
                model = Request.Model,
                messages = Messages,
                provider = Request.Provider,
                max_tokens = Request.MaxTokens,
                temperature = Request.Temperature
            )
            logging.info(Client.GenerateCompletion(Generation))
            return prompthub_pb2.PromptProcessingResponse(
                Result = prompthub_pb2.PromptMessage(
                    Role = Content["Role"],
                    Content = Content["Content"]
                )
            )
            