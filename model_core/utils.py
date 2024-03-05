import os
from tqdm import tqdm
from . import ModelResponse
from .configs  import TEXT_DIR, CHUNK_SIZE, OVERLAP, TEXT_FILENAMES
from . import (
    cohere,
    # chatglm,
    openai,
    CHATGLM_HISTORY,
    # tokenizer,
    INPUT_TEMPLATE
)
import hashlib

def generate(text_filename):
    """Generate QA for one text file"""
    contexts = generate_contexts(text_filename=text_filename)
    for context in tqdm(contexts[:3]):
        model_response = generate_question_and_answers_openai(context=context)
        model_response.save_response(output_dir="./openai-results")

def generate_question_and_answers_openai(context, show_response=True) -> ModelResponse:
    """Generate QA according to some context using LLM"""
    response = openai.generate(context=context)
    return ModelResponse(context=context, response=response)

def generate_question_and_answers_cohere(context, show_response=True) -> ModelResponse:
    """Generate QA according to some context using LLM"""
    response = ""
    for chunk in cohere.stream({"context": context}):
        if show_response:
            print(chunk.content, end="", flush=True)
        response += chunk.content
    return ModelResponse(context=context, response=response)

# def generate_question_and_answers_chatglm(context, show_response=True) -> ModelResponse:
#     try:
#         query = INPUT_TEMPLATE.format(context=context)
#         history = CHATGLM_HISTORY.copy()
#         response, _ = chatglm.chat(tokenizer, query=query, history=history, max_new_tokens=2048)
#     except Exception as e:
#         print(e.args)
#         response = ""
#     return ModelResponse(context=context, response=response)

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