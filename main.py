from text_processor.text import Text
from qa_generator.model import QAModel
from configs.processor_config import PROCESSOR_INPUT_DIR
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

text_filenames = os.listdir(PROCESSOR_INPUT_DIR)

for text_filename in text_filenames:
    if text_filename != "chapter1.tex": continue
    text_text = Text(filename=text_filename)
    text_pieces = text_text.segment(strategy="subsection")
    for text_piece in text_pieces[3:4]:

        context = text_piece.piece_info.get("content", None)
        response = {}

        if context is None:
            logging.error(f"Context in '{text_filename}' not found.")
        elif len(context) <= 300:
            logging.error(f"Context length {len(context)} too short.")
        elif len(context) >= 5000:
            logging.error(f"Context length {len(context)} too long.")
        else:
            response = QAModel.generate(context=context)

        text_piece.save_piece(response=response)
