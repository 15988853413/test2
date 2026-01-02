import os

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QSplitter, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QSettings, QDir, QByteArray

from utils.file_utils import get_document_type
from views.editor.doc_editor import DocEditor
from views.editor.html_editor import HtmlEditor
from views.editor.md_editor import MarkdownEditor
from views.editor.text_editor import TextEditor
from views.tree_view import DocumentTreeView
from models.document import DocumentType


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("个人文档管理系统")
        self.resize(1200, 800)
        self.setup_ui()
        self.setup_connections()
        self.load_settings()

    def setup_ui(self):
        # 主窗口布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 分割器
        self.splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.splitter)

        # 左侧目录树
        self.tree_view = DocumentTreeView()
        self.splitter.addWidget(self.tree_view)

        # 右侧编辑器区域
        self.editor_stack = QWidget()
        self.editor_stack.setLayout(QHBoxLayout())
        self.editor_stack.layout().setContentsMargins(0, 0, 0, 0)

        # 创建各种编辑器
        self.editors = {
            DocumentType.TEXT: TextEditor(),
            DocumentType.MARKDOWN: MarkdownEditor(),
            DocumentType.DOC: DocEditor(),
            DocumentType.HTML: HtmlEditor(),
            DocumentType.PYTHON: TextEditor(),
            DocumentType.RICH_TEXT: DocEditor()
        }

        for editor in self.editors.values():
            self.editor_stack.layout().addWidget(editor)
            editor.hide()

        self.splitter.addWidget(self.editor_stack)
        self.splitter.setSizes([300, 900])

    def setup_connections(self):
        # 连接目录树信号
        self.tree_view.document_selected.connect(self.open_document)
        self.tree_view.new_document_requested.connect(self.create_new_document)
        self.tree_view.new_directory_requested.connect(self.create_new_directory)
        self.tree_view.rename_requested.connect(self.rename_item)
        self.tree_view.delete_requested.connect(self.delete_item)

        # 连接编辑器信号
        for editor in self.editors.values():
            editor.save_requested.connect(self.save_current_document)
            editor.save_as_requested.connect(self.save_as_current_document)

    def load_settings(self):
        settings = QSettings("PersonalDocManager", "DocumentManager")

        # 加载最后路径，默认使用用户主目录
        last_path = settings.value("last_path", QDir.homePath())
        self.tree_view.set_root_path(last_path)

        # 加载窗口几何设置，带默认值和类型转换
        geometry = settings.value("window_geometry", None)
        if isinstance(geometry, (QByteArray, bytes, bytearray)):
            self.restoreGeometry(geometry)
        elif geometry is not None:  # 处理其他可能的类型
            self.restoreGeometry(QByteArray(geometry))

        # 加载窗口状态设置
        state = settings.value("window_state", None)
        if isinstance(state, (QByteArray, bytes, bytearray)):
            self.restoreState(state)
        elif state is not None:
            self.restoreState(QByteArray(state))

    # def load_settings(self):
    #     settings = QSettings("PersonalDocManager", "DocumentManager")
    #     last_path = settings.value("last_path", QDir.homePath())
    #     self.tree_view.set_root_path(last_path)
    #     self.restoreGeometry(settings.value("window_geometry"))
    #     self.restoreState(settings.value("window_state"))

    def save_settings(self):
        settings = QSettings("PersonalDocManager", "DocumentManager")
        settings.setValue("last_path", self.tree_view.model.rootPath())
        settings.setValue("window_geometry", self.saveGeometry())
        settings.setValue("window_state", self.saveState())

    # def ", self.saveState())

    def open_document(self, file_path):
        doc_type = get_document_type(file_path)
        if doc_type is (file_path):
            if doc_type is None:
                QMessageBox.warning(self, "错误", "不支持的文件类型")
                return

        # 隐藏所有编辑器
        for editor in self.editors.values():
            editor.hide()

        # 显示对应的编辑器并加载文件
        editor = self.editors[doc_type]
        editor.show()
        editor.load_file(file_path)

    def create_new_document(self, dir_path, name, doc_type_str):
        try:
            doc_type = DocumentType(doc_type_str)
            file_path = f"{dir_path}/{name}.{doc_type.value}"

            if os.path.exists(file_path):
                QMessageBox.warning(self, "错误", "文件已存在")
                return

            with open(file_path, 'w') as f:
                f.write("")

            # 刷新目录树
            index = self.tree_view.model.index(dir_path)
            self.tree_view.model.refresh(index)

            # 打开新创建的文件
            self.open_document(file_path)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"创建文件失败: {str(e)}")

    def create_new_directory(self, parent_path, name):
        try:
            dir_path = os.path.join(parent_path, name)
            os.makedirs(dir_path, exist_ok=True)

            # 刷新目录树
            index = self.tree_view.model.index(parent_path)
            self.tree_view.model.refresh(index)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"创建目录失败: {str(e)}")

    def rename_item(self, old_path, new_name):
        try:
            dir_name = os.path.dirname(old_path)
            ext = os.path.splitext(old_path)[1]
            new_path = os.path.join(dir_name, new_name + ext)

            os.rename(old_path, new_path)

            # 刷新目录树
            index = self.tree_view.model.index(dir_name)
            self.tree_view.model.refresh(index)

            # 如果重命名的是当前打开的文件，更新编辑器
            for editor in self.editors.values():
                if editor.current_file_path == old_path:
                    editor.current_file_path = new_path
                    break
        except Exception as e:
            QMessageBox.critical(self, "错误", f"重命名失败: {str(e)}")

    def delete_item(self, path, is_dir):
        try:
            if is_dir:
                import shutil
                shutil.rmtree(path)
            else:
                os.remove(path)

            # 刷新目录树
            dir_name = os.path.dirname(path)
            index = self.tree_view.model.index(dir_name)
            self.tree_view.model.refresh(index)

            # 如果删除的是当前打开的文件，关闭编辑器
            for editor in self.editors.values():
                if editor.current_file_path == path:
                    editor.hide()
                    editor.current_file_path = None
                    break
        except Exception as e:
            QMessageBox.critical(self, "错误", f"删除失败: {str(e)}")

    def save_current_document(self):
        for editor in self.editors.values():
            if editor.isVisible():
                editor.save_file()
                return True
        return False

    def save_as_current_document(self):
        for editor in self.editors.values():
            if editor.isVisible() and editor.current_file_path:
                file_path, _ = QFileDialog.getSaveFileName(
                    self, "另存为", editor.current_file_path,
                    "All Files (*);;Text Files (*.txt);;Markdown Files (*.md)"
                )
                if file_path:
                    editor.save_file(file_path)
                    # 刷新目录树
                    dir_name = os.path.dirname(file_path)
                    index = self.tree_view.model.index(dir_name)
                    self.tree_view.model.refresh(index)
                return

        QMessageBox.warning(self, "警告", "没有打开的文档可以另存为")

    def closeEvent(self, event):
        self.save_settings()
        super().closeEvent(event)