#-----------------------------------------------------------
#
# QGIS setting manager is a python module to easily manage read/write
# settings and set/get corresponding widgets.
#
# Copyright    : (C) 2013 Denis Rouzaud
# Email        : denis.rouzaud@gmail.com
#
#-----------------------------------------------------------
#
# licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this progsram; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#---------------------------------------------------------------------


from PyQt4.QtCore import QSettings, Qt
from PyQt4.QtGui import QListWidget, QButtonGroup
from qgis.core import QgsProject

from ..setting import Setting


class Stringlist(Setting):

    def __init__(self, pluginName, name, scope, defaultValue, options={}):

        setGlobal = lambda(value): QSettings(pluginName, pluginName).setValue(name, value)
        setProject = lambda(value): QgsProject.instance().writeEntry(pluginName, name, value)
        getGlobal = lambda: QSettings(pluginName, pluginName).value(name, defaultValue, type=list)
        getProject = lambda: QgsProject.instance().readListEntry(pluginName, name, defaultValue)[0]

        Setting.__init__(self, pluginName, name, scope, defaultValue, options,
                         setGlobal, setProject, getGlobal, getProject)

    def check(self, value):
        if type(value) not in (list, tuple):
            raise NameError("Setting %s must be a string list." % self.name)

    def setWidget(self, widget):
        if type(widget) == QListWidget:
            self.signal = "clicked"
            self.widgetSetMethod = self.setListBoxes
            self.widgetGetMethod = self.getListBoxes
        elif type(widget) == QButtonGroup:
            self.signal = "buttonClicked"
            self.widgetSetMethod = self.setGroupBoxes
            self.widgetGetMethod = self.getGroupBoxes
        else:
            raise NameError("SettingManager does not handle %s widgets for integers for the moment (setting: %s)" %
                            (type(widget), self.name))
        self.widget = widget

    def setListBoxes(self, value):
        if self.widget is None:
            return
        for i in range(self.widget.count()):
            item = self.widget.item(i)
            if item.text() in value:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)

    def getListBoxes(self):
        if self.widget is None:
            return
        value = []
        for i in range(self.widget.count()):
            item = self.widget.item(i)
            if item.checkState() == Qt.Checked:
                value.append(item.text())
        return value

    def setGroupBoxes(self, value):
        if self.widget is None:
            return
        for item in self.widget.buttons():
            item.setChecked(item.objectName() in value)

    def getGroupBoxes(self):
        if self.widget is None:
            return
        value = []
        for item in self.widget.buttons():
            if item.isChecked():
                value.append(item.objectName())
        return value

