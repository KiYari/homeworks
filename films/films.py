import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, QTableWidget, QHBoxLayout, QComboBox, QMenuBar, \
    QMainWindow, QDialog
import csv

from PyQt5.uic.properties import QtCore
import design
import newfilm


class Films(QMainWindow, design.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.findFilms.clicked.connect(self.sortFilms)
        self.save.clicked.connect(self.saveChange)
        self.add.clicked.connect(self.addFilm)

        # Подключение к БД
        self.con = sqlite3.connect("films.db")
        # Создание курсора
        self.cur = self.con.cursor()

        self.genres = self.cur.execute("""SELECT * FROM genres""").fetchall()
        self.genres = dict(self.genres)
        print(self.genres)

        # Выполнение запроса и получение всех результатов
        self.names = self.cur.execute("""SELECT title, genre, year, duration, id FROM Films
                WHERE  (year >= 1950)
                AND (duration >= 60) AND (duration <= 120) """).fetchall()
        title = ['Название', 'Жанр', 'Год', 'Продолжительность', 'id']
        self.table.setColumnCount(len(title))
        self.table.setHorizontalHeaderLabels(title)
        self.table.setRowCount(0)
        for i in range(len(self.names)):
            self.table.setRowCount(self.table.rowCount() + 1)
            self.table.setItem(i, 0, QTableWidgetItem(self.names[i][0]))
            self.table.setItem(i, 1, QTableWidgetItem(self.genres.get(self.names[i][1])))
            self.table.setItem(i, 2, QTableWidgetItem(str(self.names[i][2])))
            self.table.setItem(i, 3, QTableWidgetItem(str(self.names[i][3])))
            item = QTableWidgetItem(str(self.names[i][4]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(i, 4, QTableWidgetItem(item))
        self.table.resizeColumnsToContents()
        self.cur.close()

    def saveChange(self):
        self.cur = self.con.cursor()
        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                item = self.table.item(i, j)
                if j == 1:
                    if item.text().lower() != self.genres.get(self.names[i][1]):
                        new_id = self.genres.get(self.names[i][1])
                        self.cur.execute(""" UPDATE Films 
                        SET genre = ? 
                        WHERE id = ?""", (new_id, self.names[i][4]))
                else:
                    if item.text() != str(self.names[i][j]):
                        if j == 0:
                            new_set = item.text().title()
                            self.cur.execute("""UPDATE Films
                                                    SET title = ?
                                                    WHERE id = ?""", (new_set, self.names[i][4]))
                        if j == 2:
                            new_set = item.text()
                            self.cur.execute("""UPDATE Films
                                                    SET year = ?
                                                    WHERE id = ?""", (new_set, self.names[i][4]))
                        if j == 3:
                            new_set = item.text()
                            self.cur.execute("""UPDATE Films
                                                    SET duration = ?
                                                    WHERE id = ?""", (new_set, self.names[i][4]))
        self.con.commit()
        self.cur.close()

    def sortFilms(self):
        self.con = sqlite3.connect("films.db")
        self.cur = self.con.cursor()
        cur_genre = self.cur_genre.currentText()
        cur_year = self.year.value()
        cur_start = self.time_start.value()
        cur_end = self.time_end.value()
        cur_name = self.name.text().title()

        id_genre = -1
        for i in self.genres.keys():
            if cur_genre.lower() == self.genres.get(i):
                id_genre = i
        print(id_genre)

        if id_genre != -1:
            if cur_name != '':
                self.names = self.cur.execute(""" SELECT title, genre, year, duration, id FROM Films
                                            WHERE (genre = ?) AND  (year >= ?) AND (duration >= ?) AND
                                            (duration <= ?) AND title LIKE ('%' || ? || '%')""",
                                              (id_genre, cur_year, cur_start, cur_end, cur_name)).fetchall()
            else:
                self.names = self.cur.execute(""" SELECT title, genre, year, duration, id FROM Films
                                                                    WHERE (genre = ?) AND  (year >= ?) AND (duration >= ?)
                                                                     AND (duration <= ?) """,
                                              (id_genre, cur_year, cur_start, cur_end)).fetchall()
        else:
            if cur_name != '':
                self.names = self.cur.execute(""" SELECT title, genre, year, duration, id FROM Films
                                                       WHERE (year >= ?) AND (duration >= ?) AND
                                                       (duration <= ?) AND title LIKE ('%' || ? || '%')""",
                                              (cur_year, cur_start, cur_end, cur_name)).fetchall()
            else:
                self.names = self.cur.execute(""" SELECT title, genre, year, duration, id FROM Films
                                                                               WHERE (year >= ?) 
                                                                               AND (duration >= ?)
                                                                                AND (duration <= ?) """,
                                              (cur_year, cur_start, cur_end)).fetchall()

        title = ['Название', 'Жанр', 'Год', 'Продолжительность', 'id']
        self.table.setColumnCount(len(title))
        self.table.setHorizontalHeaderLabels(title)
        self.table.setRowCount(0)
        for i in range(len(self.names)):
            self.table.setRowCount(self.table.rowCount() + 1)
            self.table.setItem(i, 0, QTableWidgetItem(self.names[i][0]))
            self.table.setItem(i, 1, QTableWidgetItem(self.genres.get(self.names[i][1])))
            self.table.setItem(i, 2, QTableWidgetItem(str(self.names[i][2])))
            self.table.setItem(i, 3, QTableWidgetItem(str(self.names[i][3])))
            item = QTableWidgetItem(str(self.names[i][4]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(i, 4, QTableWidgetItem(item))
        self.cur.close()

    def addFilm(self):
        new_film = QDialog()
        new_film = uic.loadUi('newfilm.ui')
        new_film.show()
        new_film.exec_()
        self.cur = self.con.cursor()
        last_id = self.cur.execute(""" SELECT * FROM Films""").fetchall()
        last_id = len(last_id) + 1
        film_genre = 0
        # for value in self.genres.values():
        #     if newfilm.genre.currentText().lower() == value:
        #         film_genre = value

        if new_film.name.text() != '':
            self.cur.execute("""INSERT INTO Films   
                        (title, year, genre, duration) VALUES (?, ?, ?, ?)""",
                             (new_film.name.text(), new_film.year.value(),
                              film_genre,
                              new_film.duration.text()))
        self.con.commit()
        self.cur.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.cellDelete()

    def cellDelete(self):
        choose = uic.loadUi('yesno.ui')
        choose.answer.accepted.connect(self.delete)
        choose.show()
        choose.exec_()

    def delete(self):
        self.cur = self.con.cursor()
        row_id = 0
        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                if self.table.item(i, j).isSelected():
                    row_id = self.names[i][4]
        self.cur.execute("""DELETE FROM Films
                            WHERE id=?""", (row_id,))
        self.con.commit()
        self.cur.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Films()
    ex.show()
    sys.exit(app.exec_())
