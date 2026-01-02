import os
from PyQt5.QtWidgets import (
    QTreeView, QFileSystemModel, QMenu, QInputDialog, QMessageBox
)
from PyQt5.QtCore import QDir, Qt, pyqtSignal
from models.document import DocumentType


class DocumentTreeView(QTreeView):
    document_selected = pyqtSignal(str)  # 文档路径
    directory_selected = pyqtSignal(str)  # 目录路径
    new_document_requested = pyqtSignal(str, str, str)  # 目录路径, 文档名, 类型
    new_directory_requested = pyqtSignal(str, str)  # 父目录路径, 目录名
    rename_requested = pyqtSignal(str, str)  # 旧路径, 新名称
    delete_requested = pyqtSignal(str, bool)  # 路径, 是否是目录

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        self.model.setFilter(QDir.AllDirs | QDir.Files | QDir.NoDotAndDotDot)

        name_filters = [f"*.{ext.value}" for ext in DocumentType]
        self.model.setNameFilters(name_filters)
        self.model.setNameFilterDisables(False)

        self.setModel(self.model)
        self.setHeaderHidden(True)
        self.hideColumn(1)  # 隐藏大小列
        self.hideColumn(2)  # 隐藏类型列
        self.hideColumn(3)  # 隐藏修改日期列

        self.doubleClicked.connect(self.on_item_double_clicked)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def set_root_path(self, path):
        root_index = self.model.index(path)
        self.setRootIndex(root_index)

    def on_item_double_clicked(self, index):
        path = self.model.filePath(index)
        if os.path.isfile(path):
            self.document_selected.emit(path)
        else:
            self.directory_selected.emit(path)

    def show_context_menu(self, position):
        index = self.indexAt(position)
        if not index.isValid():
            return

        path = self.model.filePath(index)
        menu = QMenu()

        if os.path.isfile(path):
            # 文件右键菜单
            rename_action = menu.addAction("重命名")
            delete_action = menu.addAction("删除")
            save_as_action = menu.addAction("另存为")

            action = menu.exec_(self.viewport().mapToGlobal(position))

            if action == rename_action:
                new_name, ok = QInputDialog.getText(
                    self, "重命名", "输入新名称:",
                    text=os.path.splitext(os.path.basename(path))[0]
                )
                if ok and new_name:
                    self.rename_requested.emit(path, new_name)
            elif action == delete_action:
                reply = QMessageBox.question(
                    self, '确认删除',
                    f'确定要删除文件 "{os.path.basename(path)}" 吗?',
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    self.delete_requested.emit(path, False)
            elif action == save_as_action:
                # 另存为功能在主控制器中实现
                pass
        else:
            # 目录右键菜单
            new_file_action = menu.addAction("新建文档")
            new_dir_action = menu.addAction("新建目录")
            rename_action = menu.addAction("重命名")
            delete_action = menu.addAction("删除")
            import_action = menu.addAction("导入文件")

            action = menu.exec_(self.viewport().mapToGlobal(position))

            if action == new_file_action:
                self.show_new_document_dialog(path)
            elif action == new_dir_action:
                new_name, ok = QInputDialog.getText(
                    self, "新建目录", "输入目录名:"
                )
                if ok and new_name:
                    self.new_directory_requested.emit(path, new_name)
            elif action == rename_action:
                new_name, ok = QInputDialog.getText(
                    self, "重命名", "输入新名称:",
                    text=os.path.basename(path)
                )
                if ok and new_name:
                    self.rename_requested.emit(path, new_name)
            elif action == delete_action:
                reply = QMessageBox.question(
                    self, '确认删除',
                    f'确定要删除目录 "{os.path.basename(path)}" 及其所有内容吗?',
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    self.delete_requested.emit(path, True)
            elif action == import_action:
                # 导入功能在主控制器中实现
                pass

    def show_new_document_dialog(self, dir_path):
        doc_types = [ext.value.upper() for ext in DocumentType]
        doc_type, ok = QInputDialog.getItem(
            self, "新建文档", "选择文档类型:", doc_types, 0, False
        )
        if not ok:
            return

        doc_name, ok = QInputDialog.getText(
            self, "新建文档", "输入文档名(不带扩展名):"
        )
        if ok and doc_name:
            self.new_document_requested.emit(dir_path, doc_name, doc_type.lower())