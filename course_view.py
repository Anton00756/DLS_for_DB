from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
from compiled_ui.course_view import Ui_CourseView
from dbengine import DBEngine
from elements import *
import webbrowser

THEME_STYLE = "QPushButton { border: 5px solid; background-color: lime; border-color: blue; border-width: 5px; " \
              "border-radius: 20px; font: bold \"Times New Roman\"; font-size: 16px; min-width: 20em; padding: 5px; " \
              "margin: 2px; } QPushButton:pressed { background-color: orange; }"
ELEMENT_STYLE = "border: 5px solid; background-color: yellow; border-color: red; border-width: 5px; " \
                "border-radius: 10px; font: bold \"Times New Roman\"; font-size: 16px; min-width: 20em; " \
                "padding: 5px; margin: 2px;"


class CourseViewer(QMainWindow):
    def __init__(self, parent, db: DBEngine, user_type: int, course_id: int):
        super(CourseViewer, self).__init__(parent)
        self.ui = Ui_CourseView()
        self.ui.setupUi(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.db = db
        self.user_type = user_type
        self.course_id = course_id
        self.theme_id = None
        self.ui.centralwidget.setLayout(self.ui.verticalLayout)
        self.ui.dockWidgetContents.setLayout(self.ui.verticalLayout_2)
        half_width = QApplication.primaryScreen().availableGeometry().width() / 2
        self.ui.dockWidget.setMinimumWidth(half_width)
        self.ui.dockWidget.setMaximumWidth(half_width)
        configure_course_table(self.ui.tableWidget, 20, 1)
        configure_course_table(self.ui.tableWidget_2, 20, 1)
        configure_course_table(self.ui.tableWidget_3, 20, 1)
        self.click_func = self.open_theme
        if self.user_type == User.ADMIN or self.user_type == User.TEACHER:
            self.create_btn = QAction("Создать тему", self.ui.menubar)
            self.create_btn.triggered.connect(self.make_theme)
            self.ui.menubar.addAction(self.create_btn)
            self.name_btn = QAction("Изменить название темы", self.ui.menubar)
            self.name_btn.triggered.connect(self.change_name_function)
            self.ui.menubar.addAction(self.name_btn)
            self.move_btn = QAction("Изменить позицию темы", self.ui.menubar)
            self.move_btn.triggered.connect(self.change_pos_function)
            self.ui.menubar.addAction(self.move_btn)
            self.delete_btn = QAction("Удалить тему", self.ui.menubar)
            self.delete_btn.triggered.connect(self.delete_function)
            self.ui.menubar.addAction(self.delete_btn)
        button_action = QAction("Пользователи", self.ui.menubar)
        button_action.triggered.connect(self.course_users)
        self.ui.menubar.addAction(button_action)
        self.results_btn = QAction("Результаты", self.ui.menubar)
        self.results_btn.triggered.connect(self.get_results)
        self.ui.menubar.addAction(self.results_btn)

        self.setWindowTitle(f'[DLS] Курс "{self.db.get_course_name(self.course_id)}"')
        self.results_btn.setVisible(False)
        self.update_view()

    def get_results(self):
        results = self.db.get_my_results(self.theme_id)
        dialog = QDialog(self)
        dialog.setLayout(QVBoxLayout())
        table = QTableWidget()
        dialog.layout().addWidget(table)
        dialog.setWindowTitle("[DLS] Результаты")
        table.setRowCount(len(results))
        table.setColumnCount(1)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.horizontalHeader().setVisible(False)
        table.verticalHeader().setVisible(False)
        for index in range(len(results)):
            task_text = results[index][2].replace('\n', '\t')
            text = f'[{results[index][1]}] Вопрос №{results[index][0] + 1}: {task_text}'
            table.setCellWidget(index, 0, QLabel(f'{text[:145]}\t\t\tРезультат: '
                                                 f'{"1 балл" if results[index][3] else "0 баллов"}. Ваш ответ: '
                                                 f'"{results[index][3]}"'))
        dialog.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        dialog.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        dialog.showMaximized()

    def course_users(self):
        show_data(self, self.db.course_users(self.course_id))

    def change_pos_function(self):
        self.click_func = self.change_pos_theme

    def change_name_function(self):
        self.click_func = self.change_name_theme

    def delete_function(self):
        self.click_func = self.delete_theme

    def delete_theme(self, number):
        answer = QMessageBox.question(self, '[DLS] Удаление', "Вы точно хотите удалить эту тему?",
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if answer == QMessageBox.No:
            return
        self.db.delete_theme(self.course_id, number)
        self.theme_id = None
        self.update_view()

    def change_name_theme(self, number):
        text, ok = QInputDialog.getText(self, '[DLS] Изменение названия', 'Введите новое название темы:')
        if ok and len(text.strip()):
            self.db.change_theme_name(number, text)
            self.theme_id = None
            self.update_view()

    def change_pos_theme(self, number):
        pos, ok = QInputDialog.getInt(self, "[DLS] Изменение позиции", "Выберите позицию темы:",
                                      1, 1, self.ui.tableWidget.rowCount())
        if ok:
            self.db.change_theme_pos(self.course_id, number, pos - 1)
            self.update_view()

    def open_theme(self, number):
        self.theme_id = number
        self.update_view()

    def make_theme(self):
        text, ok = QInputDialog.getText(self, '[DLS] Новая тема', 'Введите название темы:')
        if ok and len(text.strip()):
            theme_id = self.db.add_theme(self.course_id, text.strip())
            row_count = self.ui.tableWidget.rowCount()
            btn = QPushButton(f'[{row_count + 1}] {text.strip()}')
            btn.setStyleSheet(THEME_STYLE)
            btn.clicked.connect(lambda state, ID=theme_id: self.click_func(ID))
            self.ui.tableWidget.setRowCount(row_count + 1)
            self.ui.tableWidget.setCellWidget(row_count, 0, btn)

    def task(self, data_block, number):
        if data_block == 'Занятие':
            task_info = self.db.get_lesson(number)
            if task_info[1] is not None:
                QMessageBox.about(self, f'[DLS] "{task_info[0] if task_info[0] is not None else "Занятие"}"',
                                  task_info[1])
            if task_info[2] is not None:
                webbrowser.open(task_info[2], new=2)
        else:
            try:
                task_info = self.db.get_question(number)
                if task_info[0] is None:
                    QMessageBox.warning(self, f'[DLS] Вопрос', 'Вы уже ответили на все возможные вопросы!')
                    return
                text, ok = QInputDialog.getText(self,
                                                f'[DLS] "{task_info[0] if task_info[0] is not None else "Вопрос"}"',
                                                task_info[1])
                text = text.lower().strip()
                if ok and len(text):
                    if text == task_info[2].lower().strip():
                        QMessageBox.information(self, "[DLS] Результат", "Это правильный ответ!")
                    else:
                        QMessageBox.information(self, "[DLS] Результат", "Это неправильный ответ!")
                    if self.user_type == User.STUDENT:
                        self.db.add_question_result(task_info[3], text, text == task_info[2].strip())
            except DBEngine.DBException as error:
                if error.args[0] == "NoTasks":
                    QMessageBox.warning(self, f'[DLS] Вопрос', 'Для данного вопроса отсутствует содержимое!')
                    return

    def update_theme(self, data, label, table):
        if len(data[1]):
            label.setVisible(True)
            table.setVisible(True)
            table.clear()
            table.setRowCount(len(data[1]))
            for index in range(len(data[1])):
                btn = QPushButton(f'[{data[0]} №{index + 1}]'
                                  f'{"" if data[1][index][1] is None else " " + data[1][index][1]}', table)
                btn.setStyleSheet(ELEMENT_STYLE)
                btn.clicked.connect(lambda state, d_block=data[0], ID=data[1][index][0]: self.task(d_block, ID))
                table.setCellWidget(index, 0, btn)

    def update_view(self):
        self.ui.label.setVisible(False)
        self.ui.label_2.setVisible(False)
        self.ui.tableWidget_2.setVisible(False)
        self.ui.tableWidget_3.setVisible(False)
        if self.theme_id is not None:
            self.results_btn.setVisible(True)
            self.ui.dockWidget.setWindowTitle(f'Тема "{self.db.get_theme_name(self.theme_id)}"')
            data_list = self.db.get_materials(self.theme_id)
            self.update_theme(data_list[0], self.ui.label, self.ui.tableWidget_2)
            self.update_theme(data_list[1], self.ui.label_2, self.ui.tableWidget_3)
            self.ui.statusbar.showMessage(f"Пунктов найдено: {sum(len(block[1]) for block in data_list)}")
        else:
            self.ui.dockWidget.setWindowTitle("")
            self.ui.tableWidget.clear()
            self.results_btn.setVisible(False)
            data_list = self.db.get_themes(self.course_id)
            self.ui.tableWidget.setRowCount(len(data_list))
            for index in range(len(data_list)):
                btn = QPushButton(f'[{index + 1}] {data_list[index][1]}')
                btn.setStyleSheet(THEME_STYLE)
                btn.clicked.connect(lambda state, ID=data_list[index][0]: self.click_func(ID))
                self.ui.tableWidget.setCellWidget(index, 0, btn)
            self.ui.statusbar.showMessage(f"Тем найдено: {len(data_list)}")

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Escape:
            self.click_func = self.open_theme
