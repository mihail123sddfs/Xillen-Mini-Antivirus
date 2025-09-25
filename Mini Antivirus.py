import sys
import os
import hashlib
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QListWidget, QListWidgetItem, QMessageBox, QProgressBar
)
from PyQt5.QtCore import Qt

VIRUS_SIGNATURES = {
    "eicar": "44d88612fea8a8f36de82e1278abb02f",  # EICAR test file
    # Добавь свои сигнатуры ниже
}

def md5sum(filename):
    h = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

class MiniAntivirus(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Xillen Mini Antivirus")
        self.setMinimumSize(600, 500)
        self.folder = ""
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.label = QLabel("Выберите папку для сканирования")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.btn_choose = QPushButton("Выбрать папку")
        self.btn_choose.clicked.connect(self.choose_folder)
        layout.addWidget(self.btn_choose)

        self.btn_scan = QPushButton("Сканировать")
        self.btn_scan.clicked.connect(self.scan)
        self.btn_scan.setEnabled(False)
        layout.addWidget(self.btn_scan)

        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)

        self.result_list = QListWidget()
        layout.addWidget(self.result_list)

        self.setLayout(layout)

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выбрать папку")
        if folder:
            self.folder = folder
            self.label.setText(f"Папка: {folder}")
            self.btn_scan.setEnabled(True)
            self.result_list.clear()

    def scan(self):
        if not self.folder:
            return
        self.result_list.clear()
        files = []
        for root, dirs, fs in os.walk(self.folder):
            for f in fs:
                files.append(os.path.join(root, f))
        self.progress.setMaximum(len(files))
        self.progress.setValue(0)
        self.progress.setVisible(True)
        infected = 0
        for i, path in enumerate(files, 1):
            try:
                hash_ = md5sum(path)
                found = False
                for name, sig in VIRUS_SIGNATURES.items():
                    if hash_ == sig:
                        item = QListWidgetItem(f"[Вирус] {path} — {name}")
                        item.setForeground(Qt.red)
                        self.result_list.addItem(item)
                        infected += 1
                        found = True
                        break
                if not found:
                    item = QListWidgetItem(f"[OK] {path}")
                    item.setForeground(Qt.darkGreen)
                    self.result_list.addItem(item)
            except Exception:
                item = QListWidgetItem(f"[SKIP] {path}")
                item.setForeground(Qt.darkYellow)
                self.result_list.addItem(item)
            self.progress.setValue(i)
            QApplication.processEvents()
        self.progress.setVisible(False)
        if infected:
            QMessageBox.warning(self, "Результат", f"Обнаружено вирусов: {infected}")
        else:
            QMessageBox.information(self, "Результат", "Вирусы не найдены! Всё чисто :)")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MiniAntivirus()
    win.show()
    sys.exit(app.exec_())
