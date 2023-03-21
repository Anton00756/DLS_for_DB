from PyQt5 import QtWidgets, QtCore, QtGui
from compiled_ui.registration import Ui_Registration
from dbengine import DBEngine
import re


class RegWindow(QtWidgets.QDialog):
    class RegException(Exception):
        def __init__(self, message):
            super().__init__(message)

    def __init__(self, db: DBEngine):
        super(RegWindow, self).__init__()
        self.ui = Ui_Registration()
        self.ui.setupUi(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        self.ui.pushButton.clicked.connect(self.registration)
        self.db = db

    def registration(self):
        try:
            if not re.match(r"^[\w.-]+@[\w.]{3,}$", self.ui.lineEdit.text().strip()):
                raise RegWindow.RegException("Введите корректную почту!")
            if len(self.ui.lineEdit_2.text().strip()) < 8 or len(self.ui.lineEdit_2.text().strip()) > 50:
                raise RegWindow.RegException("Пароль должен содержать не менее 8 и не более 50 символов!")
            if self.ui.lineEdit_2.text().strip() != self.ui.lineEdit_6.text().strip():
                raise RegWindow.RegException("Введённые пароли не совпадают!")
            if not len(self.ui.lineEdit_3.text().strip()) or not self.ui.lineEdit_3.text().isalpha():
                raise RegWindow.RegException("Заполните поле для фамилии буквами!")
            name = self.ui.lineEdit_3.text().strip()
            if not len(self.ui.lineEdit_4.text().strip()) or not self.ui.lineEdit_4.text().isalpha():
                raise RegWindow.RegException("Заполните поле для имени буквами!")
            name += ' ' + self.ui.lineEdit_4.text().strip()
            if len(self.ui.lineEdit_5.text().strip()):
                if not self.ui.lineEdit_5.text().isalpha():
                    raise RegWindow.RegException("Заполните поле для отчества буквами!")
                name += ' ' + self.ui.lineEdit_5.text().strip()
            self.db.add_user(self.ui.lineEdit.text().strip().lower(), self.ui.lineEdit_2.text().strip(), name)
            QtWidgets.QMessageBox.information(self, "[DLS] Регистрация", "Аккаунт успешно создан!")
            self.close()
        except DBEngine.DBException as error:
            if error.args[0] == "SameMail":
                QtWidgets.QMessageBox.warning(self, "[DLS] Ошибка регистрации",
                                              "Аккаунт с такой почтой уже существует!")
                return
            QtWidgets.QMessageBox.warning(self, "[DLS] Ошибка регистрации", error.args[0])
        except RegWindow.RegException as error:
            QtWidgets.QMessageBox.warning(self, "[DLS] Ошибка регистрации", error.args[0])
