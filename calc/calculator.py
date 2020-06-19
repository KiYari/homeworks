import sys

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QShortcut
from calc import Ui_MainWindow


class Calc(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.condition = 1
        self.result = ''
        self.eval = []
        self.input = []

        self.pushButton_n0.clicked.connect(self.zero)
        self.pushButton_n1.clicked.connect(self.one)
        self.pushButton_n2.clicked.connect(self.two)
        self.pushButton_n3.clicked.connect(self.three)
        self.pushButton_n4.clicked.connect(self.four)
        self.pushButton_n5.clicked.connect(self.five)
        self.pushButton_n6.clicked.connect(self.six)
        self.pushButton_n7.clicked.connect(self.seven)
        self.pushButton_n8.clicked.connect(self.eight)
        self.pushButton_n9.clicked.connect(self.nine)
        self.pushButton_ac.clicked.connect(self.ac)
        self.pushButton_ec.clicked.connect(self.ec)
        self.btn_left_2.clicked.connect(self.lbracket)
        self.btn_right.clicked.connect(self.rbracket)
        self.btn_share.clicked.connect(self.share)
        self.pushButton_div.clicked.connect(self.div)
        self.pushButton_mul.clicked.connect(self.mul)
        self.pushButton_sub.clicked.connect(self.sub)
        self.pushButton_add.clicked.connect(self.add)
        self.pushButton_eq.clicked.connect(self.eq)

    def enterValue(self):

        if self.condition == 1:
            self.lineEdit.setText('')
            self.condition = 0

        self.lineEdit.setText(self.lineEdit.text() + self.input)

    def eq(self):
        self.eval = self.lineEdit.text()
        try:
            self.eval = str(eval(self.eval))
        except:
            self.eval = 'Error'
        self.lineEdit.setText(self.eval)
        self.condition = 1

    def div(self):
        self.input = '/'
        self.enterValue()

    def mul(self):
        self.input = '*'
        self.enterValue()

    def sub(self):
        self.input = '-'
        self.enterValue()

    def add(self):
        self.input = '+'
        self.enterValue()

    def share(self):
        self.input = '.'
        self.enterValue()

    def rbracket(self):
        self.input = ')'
        self.enterValue()

    def lbracket(self):
        self.input = '('
        self.enterValue()

    def ac(self):
        self.lineEdit.setText('0')
        self.condition = 1

    def ec(self):
        text = self.lineEdit.text()
        if len(text) == 1:
            self.lineEdit.setText('0')
        else:
            self.lineEdit.setText(text[:-1])

    def one(self):
        self.input = '1'
        self.enterValue()

    def two(self):
        self.input = '2'
        self.enterValue()

    def three(self):
        self.input = '3'
        self.enterValue()

    def four(self):
        self.input = '4'
        self.enterValue()

    def five(self):
        self.input = '5'
        self.enterValue()

    def six(self):
        self.input = '6'
        self.enterValue()

    def seven(self):
        self.input = '7'
        self.enterValue()

    def eight(self):
        self.input = '8'
        self.enterValue()

    def nine(self):
        self.input = '9'
        self.enterValue()

    def zero(self):
        self.input = '0'
        self.enterValue()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Calc()
    ex.show()
    sys.exit(app.exec_())
