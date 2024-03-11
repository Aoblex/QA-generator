import os
import re
import json
import logging
from .utils import touch_path
from . import PROCESSOR_OUTPUT_BASE_DIR


class Piece:
    def __init__(self, source: str, content: str) -> None:
        """source: filename without extension type"""
        self.source = source
        self.content = content
    
    def save_piece(self, response: dict):
        raise NotImplementedError(f"Save function not implemented.")
    
    @property
    def piece_info(self):
        raise NotImplementedError(f"Piece information not implemented.")
    
    def __str__(self):
        return str(self.piece_info)

class ChunkPiece(Piece):
    STRATEGY = "chunk"
    def __init__(self, source: str, content: str,
                 start_index: int, end_index: int) -> None:
        super().__init__(source, content)
        self.start_index = start_index
        self.end_index = end_index
    
    @property
    def piece_info(self):
        return {
            'strategy': self.STRATEGY,
            'source': self.source,
            'start_index': self.start_index,
            'end_index': self.end_index,
            'content_length': len(self.content),
            'content': self.content,
        }
    
    @property
    def output_dir(self):
        return os.path.join(PROCESSOR_OUTPUT_BASE_DIR, self.STRATEGY, self.source, '')
    
    @property
    def filename(self):
        return f"{self.source}_{self.STRATEGY}_from_{self.start_index}_to_{self.end_index}.json"

    def save_piece(self, response:dict):
        touch_path(self.output_dir) # create path if not exist
        output_path = os.path.join(self.output_dir, self.filename)

        with open(output_path, "w") as piece:
            json.dump([self.piece_info, response], piece,
                      indent=4, ensure_ascii=False)
        
        logging.info(f"{self.STRATEGY} piece written to '{output_path}'.")



class SectionPiece(Piece):
    STRATEGY = "section"
    def __init__(self, source: str, content: str,
                 level: int, title: str):
        super().__init__(source, content)
        self.level = level
        self.title = title
    
    @property
    def piece_info(self):
        return {
            'strategy': self.STRATEGY,
            'source': self.source,
            'level': self.level,
            'title': self.title,
            'content_length': len(self.content),
            'content': self.content,
        }

    @property
    def output_dir(self):
        return os.path.join(PROCESSOR_OUTPUT_BASE_DIR, self.STRATEGY, self.source, '')
    
    @property
    def filename(self):
        alpha_digit_title = re.sub(r'[^a-zA-Z0-9 ]', '', self.title)
        processed_title = re.sub(r'\s+', '-', alpha_digit_title)
        return f"{self.source}_{self.STRATEGY}_{processed_title.lower()}.json"


    def save_piece(self, response: dict):
        touch_path(self.output_dir) # create path if not exist
        output_path = os.path.join(self.output_dir, self.filename)
        
        with open(output_path, "w") as piece:
            json.dump([self.piece_info, response], piece,
                      indent=4, ensure_ascii = False)    
        
        logging.info(f"{self.STRATEGY} piece written to '{output_path}'.")