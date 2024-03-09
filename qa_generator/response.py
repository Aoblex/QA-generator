import hashlib
import datetime
import os
import json

class ModelResponse:

    def __init__(self, context, response):
        self.context = context
        self.response = response

    @property
    def context_hash(self) -> str:
        return hashlib.sha1(self.context.encode()).hexdigest()
    
    def save_response(self, output_dir="./results", file_name="hash"):
        current_time = datetime.datetime.now()

        if file_name == "time":
            file_name = current_time.strftime("%Y-%m-%d_%H-%M-%S.json")
        elif file_name == "hash":
            file_name = f"{self.context_hash}.json"
        else:
            raise IndexError(f"Invalid file name type: {file_name}")

        output_dict = {
            "context": self.context,
            "response": self.response,
        }
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        with open(os.path.join(output_dir, file_name), "w", encoding="utf-8") as json_file:
            json.dump(output_dict, json_file, indent=4, ensure_ascii=False)