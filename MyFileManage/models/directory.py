import os
from dataclasses import dataclass
from typing import List, Optional
from .document import Document, DocumentType


@dataclass
class Directory:
    path: str
    name: str
    parent: Optional['Directory'] = None
    subdirectories: List['Directory'] = None
    documents: List[Document] = None

    def __post_init__(self):
        if self.subdirectories is None:
            self.subdirectories = []
        if self.documents is None:
            self.documents = []

    @property
    def full_path(self) -> str:
        if self.parent:
            return os.path.join(self.parent.full_path, self.name)
        return self.path

    def create_subdirectory(self, name: str) -> 'Directory':
        new_dir = Directory(path=self.full_path, name=name, parent=self)
        os.makedirs(os.path.join(self.full_path, name), exist_ok=True)
        self.subdirectories.append(new_dir)
        return new_dir

    def create_document(self, name: str, doc_type: DocumentType) -> Document:
        doc = Document.create_new(self.full_path, name, doc_type)
        self.documents.append(doc)
        return doc

    def delete(self):
        if os.path.exists(self.full_path):
            for root, dirs, files in os.walk(self.full_path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(self.full_path)

        if self.parent:
            self.parent.subdirectories.remove(self)

    def rename(self, new_name: str):
        old_path = self.full_path
        self.name = new_name
        new_path = self.full_path
        os.rename(old_path, new_path)

    def scan(self):
        """扫描目录下的文件和子目录"""
        self.subdirectories = []
        self.documents = []

        for item in os.listdir(self.full_path):
            item_path = os.path.join(self.full_path, item)
            if os.path.isdir(item_path):
                self.subdirectories.append(Directory(path=self.full_path, name=item, parent=self))
            else:
                name, ext = os.path.splitext(item)
                ext = ext[1:] if ext else ''
                try:
                    doc_type = DocumentType(ext.lower())
                    self.documents.append(Document(path=self.full_path, title=name, doc_type=doc_type))
                except ValueError:
                    continue