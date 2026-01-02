import os
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class DocumentType(Enum):
    TEXT = "txt"
    MARKDOWN = "md"
    PYTHON = "py"
    DOC = "docx"
    HTML = "html"
    RICH_TEXT = "rtf"


@dataclass
class Document:
    path: str
    title: str
    doc_type: DocumentType
    content: Optional[str] = None

    @property
    def extension(self) -> str:
        return self.doc_type.value

    @property
    def full_path(self) -> str:
        return os.path.join(self.path, f"{self.title}.{self.extension}")

    def load_content(self):
        if os.path.exists(self.full_path):
            with open(self.full_path, 'r', encoding='utf-8') as f:
                self.content = f.read()

    def save_content(self, content: str):
        self.content = content
        with open(self.full_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def delete(self):
        if os.path.exists(self.full_path):
            os.remove(self.full_path)

    @classmethod
    def create_new(cls, path: str, title: str, doc_type: DocumentType):
        doc = cls(path=path, title=title, doc_type=doc_type)
        doc.save_content("")
        return doc