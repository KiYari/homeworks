import sys
from functools import partial

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QGroupBox, QFormLayout, QLabel, QLineEdit, QComboBox, \
    QSpinBox, QCheckBox, QGridLayout, QVBoxLayout
from PyQt5.uic.properties import QtWidgets
from kfc import Ui_MainWindow


class Kfc(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.products = [
            ('Чизбургер', "burger.png", 74),
            ('Шефбургер', "burger2.png", 105),
            ('Pepsi', "pepsi.png", 65),
            ('Lipton', "lipton.jpeg", 70)
        ]

        self.widget = QWidget()
        self.layout = QGridLayout()

        for i in range(len(self.products)):
            spin = QSpinBox()
            spin.setDisabled(True)
            check = QCheckBox()
            pict = QPixmap(self.products[i][1])
            lbl = QLabel()
            lbl.setPixmap(pict)
            lbl.resize(50, 50)
            self.layout.addWidget(lbl, i, 0)
            self.layout.addWidget(QLabel(self.products[i][0] + ' - ' + str(self.products[i][2]) + 'руб.'), i, 1)
            self.layout.addWidget(check, i, 2)
            self.layout.addWidget(spin, i, 3)

        self.widget.setLayout(self.layout)
        self.main.setWidget(self.widget)

        self.pushButton.clicked.connect(self.order)

        self.checkBoxes = []
        for i in range(len(self.products)):
            self.checkBoxes.append(self.layout.itemAtPosition(i, 2).widget())

        self.spinBoxes = []
        for i in range(len(self.products)):
            self.spinBoxes.append(self.layout.itemAtPosition(i, 3).widget())

        for check in self.checkBoxes:
            check.clicked.connect(partial(self.enableSpinBox, check))

    def enableSpinBox(self, check):
        spinbox = self.spinBoxes[self.checkBoxes.index(check)]
        if check.isChecked():
            spinbox.setEnabled(True)
        else:
            spinbox.setEnabled(False)

    def order(self):
        self.plainTextEdit.setPlainText('')
        values = [i.value() for i in self.spinBoxes]
        text = ''
        all_price = 0
        outputText = '<h3 align="center">Заказ</h3><br>'
        self.plainTextEdit.appendHtml(outputText)
        for i in range(len(values)):
            if values[i] != 0:
                text = '{}     {} * {} = {} руб.'.format(self.products[i][1], values[i], self.products[i][2],
                                                         values[i] * self.products[i][2])
                all_price += values[i] * self.products[i][2]
                self.plainTextEdit.appendPlainText(text)
        price = '<br><h4> Общая стоимость: ' + str(all_price) + "руб.</h4>"
        self.plainTextEdit.appendHtml(price)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Kfc()
    ex.show()
    sys.exit(app.exec_())
