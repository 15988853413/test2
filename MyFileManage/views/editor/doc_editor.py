from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QFont
from .base_editor import BaseEditor


class DocEditor(BaseEditor):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_editor()
        self.setup_formatting_toolbar()

    def setup_editor(self):
        self.editor = QTextEdit()
        self.editor.setStyleSheet("font-family: Arial; font-size: 12pt;")
        self.editor.textChanged.connect(self.on_text_changed)
        self.layout.addWidget(self.editor)

    def setup_formatting_toolbar(self):
        # 字体选择
        self.font_family_action = self.toolbar.addAction("字体")
        # 字号选择
        self.font_size_action = self.toolbar.addAction("字号")

        # 格式按钮
        self.bold_action = self.toolbar.addAction("B")
        self.bold_action.setCheckable(True)
        self.bold_action.triggered.connect(self.toggle_bold)

        self.italic_action = self.toolbar.addAction("I")
        self.italic_action.setCheckable(True)
        self.italic_action.triggered.connect(self.toggle_italic)

        self.underline_action = self.toolbar.addAction("U")
        self.underline_action.setCheckable(True)
        self.underline_action.triggered.connect(self.toggle_underline)

        # 对齐方式
        self.align_left_action = self.toolbar.addAction("左对齐")
        self.align_center_action = self.toolbar.addAction("居中")
        self.align_right_action = self.toolbar.addAction("右对齐")

        # 列表
        self.bullet_list_action = self.toolbar.addAction("•")
        self.numbered_list_action = self.toolbar.addAction("1.")

    def toggle_bold(self):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Bold if self.bold_action.isChecked() else QFont.Normal)
        self.merge_format_on_word_or_selection(fmt)

    def toggle_italic(self):
        fmt = QTextCharFormat()
        fmt.setFontItalic(self.italic_action.isChecked())
        self.merge_format_on_word_or_selection(fmt)

    def toggle_underline(self):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(self.underline_action.isChecked())
        self.merge_format_on_word_or_selection(fmt)

    def merge_format_on_word_or_selection(self, format):
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(format)
        self.editor.mergeCurrentCharFormat(format)

    def set_content(self, content):
        self.editor.setHtml(content)

    def get_content(self):
        return self.editor.toHtml()

    def on_text_changed(self):
        self.content_changed.emit(self.get_content())