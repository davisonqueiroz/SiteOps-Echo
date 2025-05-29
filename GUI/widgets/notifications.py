from GUI.qt_core import *

class Notification():

    @staticmethod
    def info(title,text,parent = None):
        return QMessageBox.information(parent,title,text)

    @staticmethod
    def error(title,text,parent = None):
        return QMessageBox.critical(parent,title,text)