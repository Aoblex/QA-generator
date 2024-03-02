import os
from . import chain

def save_answer(filename, answer):
    filepath = os.path.join("answers", filename)
    with open(filepath, "w") as f:
        f.write(answer)

def generate_question_and_answers(context):
    answer = ""
    for chunk in chain.stream({"context": context}):
        print(chunk.content, end="", flush=True)
        answer += chunk.content
    return answer