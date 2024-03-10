from text_processor.text import Text
from qa_generator.model import QAModel
from configs.processor_config import PROCESSOR_INPUT_BASE_DIR
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# problems: 忽略练习题
IGNORED_TITLES = ['preface', 'reference', 'index', 'content', 'problems', 'exercises', 'notes']
markdown_filenames = os.listdir(PROCESSOR_INPUT_BASE_DIR)

for markdown_filename in markdown_filenames:
    if markdown_filename != "978-1-0716-1418-1.mmd":
        continue
    markdown_text = Text(filename=markdown_filename)
    # 根据 section 对文本进行分割
    markdown_sections = markdown_text.segment(strategy="section")

    for markdown_section in markdown_sections[40:45]:

        context = markdown_section.piece_info.get("content", None)
        section_title = markdown_section.piece_info.get("title", None)
        response = {}

        if context is None:
            logging.error(f"Context in '{markdown_filename}' not found.")
        elif section_title is None:
            logging.error(f"Title in '{markdown_filename}' not found.")
        elif len(context) <= 1000:
            logging.error(f"Context length {len(context)} too short.")
        elif section_title.lower() in IGNORED_TITLES:
            logging.error(f"Section title: {section_title}, irrelevant content.")
        else:
            response = QAModel.generate(context=context)

        markdown_section.save_piece(overwrite=False, response=response)
