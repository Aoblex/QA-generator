from model_core.utils import generate_question_and_answers, generate_contexts
from model_core.configs import TEXT_FILENAMES
from model_core import ModelResponse

if __name__ == "__main__":
    contexts = generate_contexts(text_filename=TEXT_FILENAMES[1])
    for context in contexts:
        model_response = generate_question_and_answers(context=context)
        model_response.save_response()
