# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ausmapAlternativeAboutDialog
                                 A QGIS plugin
 Nem adgang til ausmaps wms
                             -------------------
        begin                : 2015-05-01
        git sha              : $Format:%H$
        copyright            : (C) 2015 Agency for Data supply and Efficiency
        email                : ausmap@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
from PyQt4 import QtGui, uic

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), 'aboutausmapAlternative.ui')
)


class KFAlternativeAboutDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
