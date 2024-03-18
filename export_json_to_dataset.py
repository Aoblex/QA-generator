import os
import json

def format_response_dict(response_dict):
    formattted_dict = []
    for i in range(1, 11):
        question_i = response_dict.get(f"问题{i}", "")
        answer_i = response_dict.get(f"回答{i}", "")
        if question_i and answer_i:
            formattted_dict.append({
                "prompt": question_i,
                "query":"",
                "response": answer_i,
                "history": [],
            })
    return formattted_dict

def export_json_to_dataset(directory, output_file):
    dataset = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                with open(file_path) as f:
                    try:
                        response_str = json.load(f)[-1]["choices"][0]["message"]["content"]
                    except:
                        response_str = "{}"
                    try:
                        response_dict = json.loads(response_str)
                    except:
                        response_dict = {}
                    formatted_dict = format_response_dict(response_dict)
                    dataset.extend(formatted_dict)

    with open(output_file, "w") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=4)

# Usage example
directory = "pieces"
output_file = "statchat_dataset.json"

export_json_to_dataset(directory, output_file)