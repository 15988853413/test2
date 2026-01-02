from PyQt5.QtWidgets import QWidget, QVBoxLayout, QToolBar, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal


class BaseEditor(QWidget):
    content_changed = pyqtSignal(str)
    save_requested = pyqtSignal()
    save_as_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.current_file_path = None

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # 创建工具栏
        self.toolbar = QToolBar()
        self.layout.addWidget(self.toolbar)

        # 添加基本操作
        self.save_action = QAction(QIcon.fromTheme("document-save"), "保存", self)
        self.save_action.triggered.connect(self.save_requested.emit)
        self.toolbar.addAction(self.save_action)

        self.save_as_action = QAction(QIcon.fromTheme("document-save-as"), "另存为", self)
        self.save_as_action.triggered.connect(self.save_as_requested.emit)
        self.toolbar.addAction(self.save_as_action)

    def load_file(self, file_path):
        """加载文件内容"""
        self.current_file_path = file_path
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.set_content(content)
        except Exception as e:
            print(f"Error loading file: {e}")

    def save_file(self, file_path=None):
        """保存文件内容"""
        if file_path is None:
            file_path = self.current_file_path

        if file_path:
            try:
                content = self.get_content()
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.current_file_path = file_path
                return True
            except Exception as e:
                print(f"Error saving file: {e}")
        return False

    def set_content(self, content):
        """设置编辑器内容"""
        raise NotImplementedError

    def get_content(self):
        """获取编辑器内容"""
        raise NotImplementedError

    def setup_formatting_toolbar(self):
        """设置格式工具栏"""
        pass