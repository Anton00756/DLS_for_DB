# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/course_view.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CourseView(object):
    def setupUi(self, CourseView):
        CourseView.setObjectName("CourseView")
        CourseView.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CourseView.sizePolicy().hasHeightForWidth())
        CourseView.setSizePolicy(sizePolicy)
        CourseView.setWindowTitle("")
        self.centralwidget = QtWidgets.QWidget(CourseView)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 20, 701, 491))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        CourseView.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(CourseView)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        CourseView.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(CourseView)
        self.statusbar.setObjectName("statusbar")
        CourseView.setStatusBar(self.statusbar)
        self.dockWidget = QtWidgets.QDockWidget(CourseView)
        self.dockWidget.setWindowTitle("")
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.dockWidgetContents)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 0, 681, 243))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.tableWidget_2 = QtWidgets.QTableWidget(self.verticalLayoutWidget_2)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.verticalLayout_2.addWidget(self.tableWidget_2)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.tableWidget_3 = QtWidgets.QTableWidget(self.verticalLayoutWidget_2)
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setColumnCount(0)
        self.tableWidget_3.setRowCount(0)
        self.verticalLayout_2.addWidget(self.tableWidget_3)
        self.dockWidget.setWidget(self.dockWidgetContents)
        CourseView.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget)

        self.retranslateUi(CourseView)
        QtCore.QMetaObject.connectSlotsByName(CourseView)

    def retranslateUi(self, CourseView):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("CourseView", "Занятия"))
        self.label_2.setText(_translate("CourseView", "Вопросы"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CourseView = QtWidgets.QMainWindow()
    ui = Ui_CourseView()
    ui.setupUi(CourseView)
    CourseView.show()
    sys.exit(app.exec_())