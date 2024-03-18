from text_processor.text import Text
from qa_generator.model import QAModel
from configs.processor_config import PROCESSOR_INPUT_DIR
from configs.model_config import MODEL_CONFIGS
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

text_filenames = os.listdir(PROCESSOR_INPUT_DIR)

for text_filename in text_filenames:
    # if text_filename != "chapter1.tex": continue
    text_text = Text(filename=text_filename)
    text_pieces = text_text.segment(strategy="subsection")
    for text_piece in text_pieces:

        context = text_piece.piece_info.get("content", None)
        response = {}

        if context is None:
            logging.error(f"Context in '{text_filename}' not found.")
        elif len(context) <= 300:
            logging.error(f"Context length {len(context)} too short.")
        elif len(context) >= 6000:
            logging.error(f"Context length {len(context)} too long.")
        elif text_piece.file_exists():
            logging.info(f"'{text_piece.filename}' already exists.")
        else:
            while True:
                try: 
                    response = QAModel.generate(context=context, model_configs=MODEL_CONFIGS)
                    text_piece.append_to_file(element=response)
                    break
                except Exception as e:
                    logging.error(f"Error in generating '{text_piece.filename}'.")
