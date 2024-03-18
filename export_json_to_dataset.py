import os
import json
import re

escape_dict={
    '\a':r'\a',
    '\b':r'\b',
    '\f':r'\f',
    '\n':r'\n',
    '\r':r'\r',
    '\t':r'\t',
    '\v':r'\v',
    '\'':r'\'',
    '\"':r'\"',
    '\0':r'\0',
    '\1':r'\1',
    '\2':r'\2',
    '\3':r'\3',
    '\4':r'\4',
    '\5':r'\5',
    '\6':r'\6',
    '\7':r'\7',
}

# return a raw string using the escape_dict
def raw(text):
    new_string = ""
    for char in text:
        try: new_string += escape_dict[char]
        except KeyError: new_string += char
    return new_string

def repetition_index(s):
    # 找到所有的重复子串
    matches = re.findall(r"(.+)(\1+)", s)

    # 计算重复子串的总长度
    total_length = sum(len(match[0]) * (len(match[1]) // len(match[0])) for match in matches)

    # 计算重复程度的指标
    return total_length / len(s) if s else 0

def format_response_dict(response_dict):
    formatted_dict = []
    filter_functions = [
        filter_reference,
        filter_repetition,
        filter_keywords,
    ]
    for i in range(1, 11):
        question_i = raw(response_dict.get(f"问题{i}", ""))
        answer_i = raw(response_dict.get(f"回答{i}", ""))

        if question_i and answer_i:
            formatted_dict.append({
                "prompt": question_i,
                "query":"",
                "response": answer_i,
                "history": [],
                "repetition_index": max(repetition_index(question_i),repetition_index(answer_i)),
            })
    for filter_function in filter_functions: 
        formatted_dict = list(filter(filter_function, formatted_dict))
    return formatted_dict

def filter_repetition(response_dict):
    threshold = 0.17
    if response_dict["repetition_index"] > threshold:
        return False
    return True

def filter_keywords(response_dict):
    keywords_pattern = r"(在.*?例子中?)|(根据给定的)|(在图示中)"
    if re.search(keywords_pattern, response_dict["prompt"]):
        return False
    if re.search(keywords_pattern, response_dict["response"]):
        return False
    return True

def filter_reference(response_dict):
    reference_pattern = r"(例|例题|例子|图表|表|定理|公式|表格|性质|图|式|算法)\s*\(?\s*\d+\.\d+"
    if re.search(reference_pattern, response_dict["prompt"]):
        return False
    if re.search(reference_pattern, response_dict["response"]):
        return False
    return True

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
    # dataset.sort(key=lambda x: x["repetition_index"], reverse=True)
    for item in dataset:
        item.pop("repetition_index")
    with open(output_file, "w") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=4)

# Usage example
directory = "pieces"
output_file = "statchat_dataset.json"

export_json_to_dataset(directory, output_file)