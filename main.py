from text_processor.text import Text
from qa_generator.model import QAModel
from configs.processor_config import PROCESSOR_INPUT_DIR
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

markdown_filenames = os.listdir(PROCESSOR_INPUT_DIR)

for markdown_filename in markdown_filenames:
    markdown_text = Text(filename=markdown_filename)
    markdown_pieces = markdown_text.segment(strategy="section")

    for markdown_piece in markdown_pieces:

        context = markdown_piece.piece_info.get("content", None)
        response = {}

        if context is None:
            logging.error(f"Context in '{markdown_filename}' not found.")
        elif len(context) <= 1000:
            logging.error(f"Context length {len(context)} too short.")
        else:
            response = QAModel.generate(context=context)

        markdown_piece.save_piece(response=response)
