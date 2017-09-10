import os
from PyQt4 import QtGui, uic

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), 'aboutAusMapAlternative.ui')
)


class KFAlternativeAboutDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
