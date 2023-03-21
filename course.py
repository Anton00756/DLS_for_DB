from PyQt5 import QtWidgets, QtCore, QtGui
from compiled_ui.course import Ui_Course
from dbengine import DBEngine


class CourseCreator(QtWidgets.QDialog):
    def __init__(self, db: DBEngine):
        super(CourseCreator, self).__init__()
        self.ui = Ui_Course()
        self.ui.setupUi(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        self.ui.pushButton.clicked.connect(self.create_course)
        self.db = db

    def create_course(self):
        if not len(self.ui.lineEdit.text().strip()):
            QtWidgets.QMessageBox.warning(self, "[DLS] Ошибка создания курса", "Заполните поле для названия!")
            return
        if len(self.ui.lineEdit_3.text()) and not self.ui.lineEdit_3.text().isdigit():
            QtWidgets.QMessageBox.warning(self, "[DLS] Ошибка создания курса", "Некорректный номер курса института!")
            return
        self.db.create_course(self.ui.lineEdit.text().strip(), self.ui.lineEdit_2.text().strip(),
                              self.ui.lineEdit_3.text().strip())
        self.close()
