from model_core.utils import (
    generate_question_and_answers_cohere,
    generate_contexts,
    generate_question_and_answers_chatglm,
    generate,
)
from model_core.configs import TEXT_FILENAMES
from model_core import ModelResponse
from tqdm import tqdm

if __name__ == "__main__":
    for text_filename in TEXT_FILENAMES[2:]:
        print(f"Generating QA for '{text_filename}'")
        generate(text_filename)