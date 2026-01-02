import os
from typing import Optional

from models.document import DocumentType


def import_file(src_path: str, dest_dir: str) -> Optional[str]:
    """导入文件到目标目录"""
    if not os.path.exists(src_path):
        return None

    filename = os.path.basename(src_path)
    dest_path = os.path.join(dest_dir, filename)

    if os.path.exists(dest_path):
        base, ext = os.path.splitext(filename)
        counter = 1
        while True:
            new_filename = f"{base}_{counter}{ext}"
            new_dest_path = os.path.join(dest_dir, new_filename)
            if not os.path.exists(new_dest_path):
                dest_path = new_dest_path
                break
            counter += 1

    try:
        with open(src_path, 'rb') as src_file, open(dest_path, 'wb') as dest_file:
            dest_file.write(src_file.read())
        return dest_path
    except Exception as e:
        print(f"Error importing file: {e}")
        return None


def get_document_type(filename: str) -> Optional[DocumentType]:
    """根据文件名获取文档类型"""
    _, ext = os.path.splitext(filename)
    ext = ext[1:] if ext else ''
    try:
        return DocumentType(ext.lower())
    except ValueError:
        return None