from text_processor.text import Text
from qa_generator.model import QAModel
from configs.processor_config import PROCESSOR_INPUT_BASE_DIR
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

IGNORED_TITLES = ['preface', 'reference', 'index', 'content', 'problems']
markdown_filenames = os.listdir(PROCESSOR_INPUT_BASE_DIR)

for markdown_filename in markdown_filenames[1:3]:
    markdown_text = Text(filename=markdown_filename)
    markdown_sections = markdown_text.segment(strategy="section")

    for markdown_section in markdown_sections[10:12]:

        context = markdown_section.piece_info.get("content", None)
        if context is None:
            logging.error(f"Context in '{markdown_filename}' not found.")

        section_title = markdown_section.piece_info.get("title", None)
        if section_title is None:
            logging.error(f"Title in '{markdown_filename}' not found.")

        if context and section_title \
           and section_title.lower() not in IGNORED_TITLES:
            raw_response = QAModel.generate(context=context)
        else:
            raw_response = ""

        markdown_section.save_piece(overwrite=True, raw_response=raw_response)
