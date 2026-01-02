from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSplitter, QTextEdit, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from markdown import markdown
from .base_editor import BaseEditor


class MarkdownEditor(BaseEditor):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_editor()
        self.setup_markdown_toolbar()

    def setup_editor(self):
        self.splitter = QSplitter(Qt.Vertical)
        self.layout.addWidget(self.splitter)

        # 编辑器
        self.editor = QTextEdit()
        self.editor.setStyleSheet("font-family: Consolas; font-size: 12pt;")
        self.editor.textChanged.connect(self.on_text_changed)

        # 预览
        self.preview = QWebEngineView()

        self.splitter.addWidget(self.editor)
        self.splitter.addWidget(self.preview)
        self.splitter.setSizes([300, 300])

    def setup_markdown_toolbar(self):
        # 添加Markdown专用工具栏按钮
        bold_action = self.toolbar.addAction("B")
        bold_action.setToolTip("加粗")
        bold_action.triggered.connect(self.insert_bold)

        italic_action = self.toolbar.addAction("I")
        italic_action.setToolTip("斜体")
        italic_action.triggered.connect(self.insert_italic)

        header_action = self.toolbar.addAction("H")
        header_action.setToolTip("标题")
        header_action.triggered.connect(self.insert_header)

        list_action = self.toolbar.addAction("•")
        list_action.setToolTip("列表")
        list_action.triggered.connect(self.insert_list)

        link_action = self.toolbar.addAction("🔗")
        link_action.setToolTip("链接")
        link_action.triggered.connect(self.insert_link)

    def insert_bold(self):
        self.editor.insertPlainText("**bold text**")

    def insert_italic(self):
        self.editor.insertPlainText("*italic text*")

    def insert_header(self):
        self.editor.insertPlainText("## Header")

    def insert_list(self):
        self.editor.insertPlainText("- List item")

    def insert_link(self):
        self.editor.insertPlainText("[text](url)")

    def set_content(self, content):
        self.editor.setPlainText(content)
        self.update_preview()

    def get_content(self):
        return self.editor.toPlainText()

    def on_text_changed(self):
        content = self.get_content()
        self.content_changed.emit(content)
        self.update_preview()

    def update_preview(self):
        html = markdown(self.get_content())
        self.preview.setHtml(html)