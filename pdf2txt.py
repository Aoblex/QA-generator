from unstructured.partition.auto import partition
from unstructured.partition.pdf import partition_pdf
import unstructured.documents.elements
import os
import re

os.environ["http_proxy"]="http://127.0.0.1:7890"
os.environ["https_proxy"]="http://127.0.0.1:7890"

text_dir = os.path.join(os.getcwd(), "text")
pdf_dir = os.path.join(os.getcwd(), "pdf")
filenames = [filename for filename in os.listdir(pdf_dir)
             if re.match(r'^(.*?)\.pdf$', filename)] # match all pdf files

def convert_pdf_to_text(pdf_filename):
    pdf_path = os.path.join(pdf_dir, pdf_filename)
    text_filename = f"{filename.split('.')[0]}.txt"
    text_path = os.path.join(text_dir, text_filename)
    if not os.path.exists(text_path):
        elements = partition_pdf(filename=pdf_path,
                             strategy="fast")
        with open(text_path, "w") as f:
            f.write("".join([element.text for element in elements]))
        print(f"'{pdf_filename}' converted to '{text_filename}'")
    else:
        print(f"'{text_filename}' already exists.")
    return 1

for filename in filenames:
    convert_pdf_to_text(filename)