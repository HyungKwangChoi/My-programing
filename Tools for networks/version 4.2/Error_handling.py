
from PyQt5 import QtWidgets

def pop_up_error(exception_error_messages):
            error_msg = QtWidgets.QMessageBox()
            error_msg.setIcon(QtWidgets.QMessageBox.Critical)
            error_msg.setWindowTitle("Error")
            error_msg.setDetailedText("")
            error_msg.setText(str(exception_error_messages))
            error_msg.exec_() 