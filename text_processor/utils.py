import os

def touch_path(file_path):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

def is_file_path(file_path):
    return os.path.exists(file_path)

def is_text_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    text_extensions = ['.md', '.mmd', '.txt', '.py', '.html', '.xml', '.tex']  # 添加其他可能的文本文件扩展名
    return file_extension.lower() in text_extensions
