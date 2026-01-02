from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QSplitter, QTextEdit, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt

from views.editor.base_editor import BaseEditor


class HtmlEditor(BaseEditor):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_editor()  # 确保这里的方法名正确
        self.setup_html_toolbar()

    def setup_editor(self):
        self.splitter = QSplitter(Qt.Horizontal)
        self.layout.addWidget(self.splitter)

        # HTML编辑器
        self.editor = QTextEdit()
        self.editor.setStyleSheet("font-family: Consolas; font-size: 12pt;")
        self.editor.textChanged.connect(self.on_text_changed)

        # 预览
        self.preview = QWebEngineView()

        self.splitter.addWidget(self.editor)
        self.splitter.addWidget(self.preview)
        self.splitter.setSizes([300, 300])

    def setup_html_toolbar(self):
        # 添加HTML专用工具栏按钮
        tag_actions = [
            ("<p>", "段落"), ("<h1>", "标题1"), ("<div>", "Div"),
            ("<a>", "链接"), ("<img>", "图片"), ("<table>", "表格")
        ]

        for tag, tooltip in tag_actions:
            action = self.toolbar.addAction(tag)
            action.setToolTip(tooltip)
            action.triggered.connect(lambda _, t=tag: self.insert_html_tag(t))

    def insert_html_tag(self, tag):
        cursor = self.editor.textCursor()
        cursor.insertText(f"<{tag}></{tag}>")
        cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, len(tag) + 3)
        self.editor.setTextCursor(cursor)

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
        self.preview.setHtml(self.get_content())