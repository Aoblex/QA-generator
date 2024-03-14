import os
import re
from typing import List
from .pieces import Piece, SectionPiece, ChunkPiece, SubsectionPiece
from .utils import is_file_path, is_text_file
from . import PROCESSOR_INPUT_DIR

class Text:

    SEGMENT_STRATEGIES = ["section", "chunk", "subsection"]

    def __init__(self, filename: str, dir: str = PROCESSOR_INPUT_DIR):
        """Load on initialization"""
        self.dir = dir
        self.filename = filename
        self.source = filename.split(".")[0]
        self.file_path = os.path.join(dir, filename)

        if not is_file_path(self.file_path):
            raise FileNotFoundError(f"The file '{self.file_path}' does not exist.")
        
        if not is_text_file(self.file_path):
            raise TypeError(f"'{self.filename}' is not a text file.")
        
        with open(self.file_path, "r") as text_file:
            self.content = text_file.read()

    def segment_into_sections(self) -> List[Piece]:
        """Segment the original content into sections by '#'."""
        pattern = re.compile(r'^(#+)\s+(.*?)\s*$(.*?)(?=(?:^#+\s+|\Z))',
                            re.MULTILINE | re.DOTALL)
        matches = pattern.findall(self.content)

        # Segmenting
        sections = []
        for level, title, content in matches:
            final_content = f"Title: {title}\nContent: {content.strip()}"
            sections.append(SectionPiece(
                source = self.source,
                content = final_content,
                level = len(level),
                title = title.strip(),
            ))
        
        return sections

    def segment_into_subsections(self) -> List[Piece]:
        """Segment the original content into subsections."""

        # Remove xiti
        xiti_pattern = r'\\begin\{xiti\}([\s\S]*?)\\end\{xiti\}'
        self.content = re.sub(xiti_pattern, '', self.content)

        pattern = re.compile(r'\\subsection\{([^}]+)\}([\s\S]*?)(?=\\subsection|\Z)',
                             re.MULTILINE | re.DOTALL)
        matches = pattern.findall(self.content)

        # Segmenting
        subsections = []
        for title, content in matches:
            final_content = f"Title: {title}\nContent: {content.strip()}"
            subsections.append(SubsectionPiece(
                source = self.source,
                content = final_content,
                title = title.strip(),
            ))
        
        return subsections

    def segment_into_chunks(self, **kwargs) -> List[Piece]:
        """Segment the original content into chunks."""
        chunk_length = kwargs.pop("chunk_length", 300)
        overlap = kwargs.pop("overlap", 50)
        assert chunk_length > overlap, f"chunk_length={chunk_length} <= overlap={overlap}"

        # Segmenting
        chunks, start_index = [], 0
        while start_index < len(self.content):
            end_index = start_index + chunk_length
            chunks.append(ChunkPiece(
                source = self.source,
                content = self.content.strip(),
                start_index = start_index,
                end_index = end_index,
            ))
            start_index += chunk_length - overlap

        return chunks

    def segment(self, strategy: str) :
        """Segment the original content according to a specific strategy.\n
        strategy must be in ['section', 'chunk', 'subsection']"""
        assertion_error_message = f"Unsupported strategy type: {strategy}"
        assert strategy in self.SEGMENT_STRATEGIES, assertion_error_message

        if strategy == "section":
            return self.segment_into_sections()
        elif strategy == "chunk":
            return self.segment_into_chunks()
        elif strategy == "subsection":
            return self.segment_into_subsections()
        else:
            raise AssertionError(assertion_error_message)