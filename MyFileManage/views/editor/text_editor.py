from PyQt5.QtWidgets import QPlainTextEdit
from .base_editor import BaseEditor


class TextEditor(BaseEditor):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_editor()

    def setup_editor(self):
        self.editor = QPlainTextEdit()
        self.editor.setStyleSheet("font-family: Consolas; font-size: 12pt;")
        self.editor.textChanged.connect(self.on_text_changed)
        self.layout.addWidget(self.editor)

    def set_content(self, content):
        self.editor.setPlainText(content)

    def get_content(self):
        return self.editor.toPlainText()

    def on_text_changed(self):
        self.content_changed.emit(self.get_content())