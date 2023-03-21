from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QHeaderView, QDialog, QVBoxLayout, QLabel


class User(int):
    STUDENT = 0
    TEACHER = 1
    MANAGER = 2
    ADMIN = 3


def configure_course_table(table: QTableWidget, row: int, column: int):
    table.setRowCount(row)
    table.setColumnCount(column)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
    table.horizontalHeader().setVisible(False)
    table.verticalHeader().setVisible(False)
    table.setShowGrid(False)


def show_data(parent, users):
    dialog = QDialog(parent)
    dialog.setLayout(QVBoxLayout())
    table = QTableWidget()
    dialog.layout().addWidget(table)
    dialog.setWindowTitle("[DLS] Просмотр пользователей")
    table.setRowCount(len(users))
    table.setColumnCount(1)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    table.horizontalHeader().setVisible(False)
    table.verticalHeader().setVisible(False)
    for index in range(len(users)):
        table.setCellWidget(index, 0, QLabel(f'{users[index][0]}: {users[index][1]}. \tПоследний вход: '
                                             f'{users[index][2]}.'
                                             f'{" " + users[index][3] if users[index][3] is not None else ""}'))
    dialog.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
    dialog.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
    dialog.showMaximized()
