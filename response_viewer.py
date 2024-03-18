import os
import json
from configs.processor_config import PROCESSOR_OUTPUT_BASE_DIR

piecing_strategy = "subsection"
text_file = "chapter1"

piece_dir = os.path.join(PROCESSOR_OUTPUT_BASE_DIR, piecing_strategy, text_file, "")

json_data = {}
for piece_name in os.listdir(piece_dir):
    piece_path = os.path.join(piece_dir, piece_name)
    with open(piece_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        responses = []
        for response in data[1:]:
            first_choice = response.get("choices", [{}])[0]
            message = first_choice.get("message", {})
            content = message.get("content", r"{}")
            try:
                responses.append(json.loads(content))
            except:
                responses.append({"response": content})
    json_data[piece_name] = responses

for piece_name, responses in json_data.items():
    print("-"*20,f"[{piece_name}]", "-"*20)
    for response in responses:
        for i, item in enumerate(response.items()):
            k, v = item
            print(k, v)
            if i%2:
                print("-"*50)