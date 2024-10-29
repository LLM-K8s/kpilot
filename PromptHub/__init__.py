from concurrent import futures
import grpc
import prompthub_pb2
import prompthub_pb2_grpc
import json

class PromptManager():
    def __init__(self):
        self.jsonfile = "./data/repository.json"
        self.prompts = {}
        self.openfile()

    # 讀取prompts
    def openfile(self):
        with open(self.jsonfile, encoding="utf-8") as f:
            content = f.read()
            self.prompts = json.loads(content)
            print(f"Prompt內容：{self.prompts}")

    # 儲存prompts
    def savefile(self):
        with open(self.jsonfile, "w", encoding="utf-8") as f:
            json.dump(self.prompts, f, indent=4, ensure_ascii = False)

    # 新增
    def add(self, request, context) -> str:
        # 避免重複新增相同名稱而覆蓋
        if request.Name not in self.prompts.keys():
            self.prompts[request.Name] = request.Prompt
            print(f"{request.Name}，新增成功!")
            self.savefile() # 儲存prompts
            return prompthub_pb2.AddResponse(AddOutput = f"{request.Name}，新增成功!")
        else:
            print(f"{request.Name}，新增失敗，請檢查是否為重複名稱!")
            return prompthub_pb2.AddResponse(AddOutput = f"{request.Name}，新增失敗，請檢查是否為重複名稱!")

    # 修改
    def update(self, request, context) -> str:
        if request.Name in self.prompts:
            self.prompts[request.Name] = request.new_prompt
            print(f"成功修改{request.Name}")
            self.savefile() # 儲存prompts
            return prompthub_pb2.UpdateResponse(UpdateOutput = f"成功修改{request.Name}，內容：{self.prompts[request.Name]}")
        else:
            print(f"提示詞 '{request.Name}' 未找到。")
            return prompthub_pb2.UpdateResponse(UpdateOutput = f"提示詞 '{request.Name}' 未找到。")

    # 刪除
    def delete(self, request, context) -> str:
        if request.Name in self.prompts:
            del self.prompts[request.Name]
            self.savefile() # 儲存prompts
            return prompthub_pb2.DeleteResponse(DeleteOutput = f"成功刪除{request.Name}")
        else:
            print(f"提示詞 '{request.Name}' 未找到。")
            return prompthub_pb2.DeleteResponse(DeleteOutput = f"提示詞 '{request.Name}' 未找到。")

    # 取得prompt的內容
    def get(self, request, context) -> str:
        result = self.prompts.get(request.Name, f"提示詞 '{request.Name}' 未找到。")
        print(result)
        return prompthub_pb2.GetResponse(GetOutput = f"{result}")

    # 列出所有的prompt
    def list(self, request, context) -> str:
        result = ""
        items = self.prompts.items()
        print(items)
        for index, (name, prompt) in enumerate(items):
            result += f"{index + 1}. 模板名稱：{name}, 內容：{prompt}\n"
        print(result)
        return prompthub_pb2.ListResponse(ListOutput = f"{result}")

    
    # 列出指定的prompt
    def select(self, request, context) -> str:
        try:
            selected_name = list(self.prompts.keys())[int(request.Number) - 1]
            print(f"{selected_name}, {self.prompts[selected_name]}")
            return(prompthub_pb2.SelectResponse(SelectOutput = f"模板名稱：{selected_name}, 內容：{self.prompts[selected_name]}"))
        except IndexError:
            pass
            print("查無此資料。")
            return prompthub_pb2.SelectResponse(SelectOutput = "查無此資料。")
        
    # 把結果輸出給LLM (待製作)
    def output(self) -> str:
        pass

def run_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    prompthub_pb2_grpc.add_simpleServicer_to_server(PromptManager(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    run_server()