import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.uic.properties import QtWidgets
from html import Ui_MainWindow


class Editor(Ui_MainWindow, QMainWindow):

    def __init__(self):
        super(Editor, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.translate)

    def translate(self):
        text = self.plainTextEdit.toPlainText()
        self.textBrowser.setText(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Editor()
    ex.show()
    sys.exit(app.exec_())
