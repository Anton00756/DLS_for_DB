from PyQt5 import QtWidgets, QtCore, QtGui
from compiled_ui.login import Ui_Login
from registration import RegWindow
from dbengine import DBEngine


class LogWindow(QtWidgets.QDialog):
    user_login = QtCore.pyqtSignal(int)

    def __init__(self, db: DBEngine):
        super(LogWindow, self).__init__()
        self.ui = Ui_Login()
        self.ui.setupUi(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        self.ui.pushButton.clicked.connect(self.login)
        self.ui.pushButton_2.clicked.connect(self.registration_window)
        self.db = db

    def registration_window(self):
        registration = RegWindow(self.db)
        registration.exec_()

    def login(self):
        try:
            person_type = self.db.login(self.ui.lineEdit.text().strip().lower(), self.ui.lineEdit_2.text().strip())
            if person_type is None:
                QtWidgets.QMessageBox.warning(self, "[DLS] Ошибка входа",
                                              "Некорректный логин или пароль!\nПопробуйте ещё :)")
            else:
                self.user_login.emit(person_type)
                self.close()
        except DBEngine.DBException as error:
            QtWidgets.QMessageBox.warning(self, "[DLS] Ошибка входа", error.args[0])
