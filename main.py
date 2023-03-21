import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
from compiled_ui.main_page import Ui_MainWindow
from course import CourseCreator
from login import LogWindow
from course_view import CourseViewer
from dbengine import DBEngine
from elements import *


#  python -m PyQt5.uic.pyuic -x ui/login.ui -o compiled_ui/login.py
#  python -m PyQt5.uic.pyuic -x ui/registration.ui -o compiled_ui/registration.py
#  python -m PyQt5.uic.pyuic -x ui/main_page.ui -o compiled_ui/main_page.py
#  python -m PyQt5.uic.pyuic -x ui/course.ui -o compiled_ui/course.py
#  python -m PyQt5.uic.pyuic -x ui/course_view.ui -o compiled_ui/course_view.py


class DLSapp(QMainWindow):
    def __init__(self):
        super(DLSapp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.db = DBEngine()

        self.user_type = None
        self.hide()
        login = LogWindow(self.db)
        login.user_login.connect(self.set_user)
        login.exec_()
        if self.user_type is None:
            self.db.close()
            quit(0)
        self.db.update_log()

        self.reload_actions()
        self.setCentralWidget(self.ui.tabWidget)
        self.ui.tabWidget.tabBarClicked.connect(self.update_courses)

        self.ui.tab.setLayout(self.ui.verticalLayout)
        self.ui.tab_2.setLayout(self.ui.verticalLayout_2)
        configure_course_table(self.ui.tableWidget, 5, 3)
        configure_course_table(self.ui.tableWidget_2, 5, 3)
        self.update_courses(0)
        self.showMaximized()

    def reload_actions(self):
        self.ui.menubar.clear()
        if self.user_type == User.STUDENT:
            button_action = QAction(QtGui.QIcon("images/crown.png"), "", self.ui.menubar)
            button_action.triggered.connect(self.make_admin)
            self.ui.menubar.addAction(button_action)
        if self.user_type == User.ADMIN or self.user_type == User.TEACHER:
            button_action = QAction("Создать курс", self.ui.menubar)
            button_action.triggered.connect(self.make_course)
            self.ui.menubar.addAction(button_action)
        button_action = QAction("Пользователи", self.ui.menubar)
        button_action.triggered.connect(self.all_users)
        self.ui.menubar.addAction(button_action)
        button_action = QAction("О пользователе", self.ui.menubar)
        button_action.triggered.connect(self.information)
        self.ui.menubar.addAction(button_action)

        # bar = self.menuBar()
        # file_menu = bar.addMenu('File')
        # open_action = QtWidgets.QAction('Open', self)
        # close_action = QtWidgets.QAction('Close', self)
        # file_menu.addAction(open_action)
        # file_menu.addAction(close_action)

    def all_users(self):
        show_data(self, self.db.get_all_users())

    def make_course(self):
        course = CourseCreator(self.db)
        course.exec_()
        self.update_courses(self.ui.tabWidget.currentIndex())

    def update_courses(self, page):
        if not page:
            courses = self.db.get_all_courses()
            table = self.ui.tableWidget
        else:
            courses = self.db.get_my_courses()
            table = self.ui.tableWidget_2
        index = 0
        for course in courses:
            course_text = course[1]
            if course[2] is not None:
                course_text += f'\n[{course[2]}' + (']' if course[3] is None else f'; {course[3]} курс]')
            elif course[3] is not None:
                course_text += f'\n[{course[3]} курс]'
            btn = QPushButton(course_text)
            btn.setStyleSheet("border: 5px solid; background-color: #E8E8E8; border-top-color: red;"
                              "border-left-color: blue; border-right-color: yellow; border-bottom-color: green;"
                              "border-width: 5px; border-radius: 30px; font: bold \"Times New Roman\"; font-size: 17px;"
                              "min-width: 10em; padding: 10px; margin: 3px")
            btn.clicked.connect(lambda state, course_page=page, course_id=course[0]: self.open_course(course_page,
                                                                                                      course_id))
            table.setCellWidget(index // 3, index % 3, btn)
        self.ui.statusbar.showMessage(f"Курсов найдено: {len(courses)}")

    def open_course(self, page, number):
        if not page and not self.db.course_is_my(number):
            answer = QMessageBox.question(self, '[DLS] Подключение', "Хотите присоединиться к данному курсу?",
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if answer == QMessageBox.No:
                return
            self.db.connect_to_course(number)
        else:
            self.db.update_course_log(number)
        course_viewer = CourseViewer(self, self.db, self.user_type, number)
        course_viewer.showMaximized()

    def information(self):
        QMessageBox().about(self, "[DLS] О пользователе", self.db.get_person_info())

    def make_admin(self):
        text, ok = QInputDialog.getText(self, '[DLS] Получение админки', 'Введите пароль:', QLineEdit.EchoMode.Password)
        if ok and text == "admin":
            self.db.make_admin(User.ADMIN)
            self.user_type = User.ADMIN
            self.reload_actions()

    def set_user(self, user_type):
        self.user_type = user_type

    def closeEvent(self, event):
        self.db.close()
        event.accept()


app = QApplication([])
application = DLSapp()  # tosha@mail.ru 05082002
application.show()
sys.exit(app.exec())
