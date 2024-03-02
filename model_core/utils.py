import os
from . import ModelResponse
from .configs  import TEXT_DIR, CHUNK_SIZE, OVERLAP
from . import cohere 

def generate_question_and_answers_cohere(context, show_response=True) -> ModelResponse:
    """Generate QA according to some context using LLM"""
    response = ""
    for chunk in cohere.stream({"context": context}):
        if show_response:
            print(chunk.content, end="", flush=True)
        response += chunk.content
    return ModelResponse(context=context, response=response)

def generate_contexts(text_filename):
    """Generate context pieces for a text file"""
    contexts = []
    with open(os.path.join(TEXT_DIR, text_filename), "r") as f:
        text = f.read()
        head_index = 0
        while head_index < len(text):
            contexts.append(text[head_index:head_index + CHUNK_SIZE])
            head_index += CHUNK_SIZE - OVERLAP 
    return contexts