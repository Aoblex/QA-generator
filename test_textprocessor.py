from text_processor.text import Text
from text_processor.pieces import SubsectionPiece

text = Text("chapter1.tex")
subsections = text.segment("subsection")
for subsection in subsections:
    print((subsection.content))
    print("="*60)