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
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#---------------------------------------------------------------------

from PyQt4.QtCore import QObject, pyqtSignal


class Setting(QObject):
    valueChanged = pyqtSignal()

    def __init__(self, pluginName, name, scope, defaultValue, options, setGlobal, setProject, getGlobal, getProject):
        QObject.__init__(self)
        self.pluginName = pluginName
        self.name = name
        self.scope = scope
        self.defaultValue = defaultValue
        self.widget = None
        self.options = options
        self.setGlobal = setGlobal
        self.setProject = setProject
        self.getGlobal = getGlobal
        self.getProject = getProject

        self.check(defaultValue)

    def check(self, value):
        """
        This method shall be overriden in type subclasses
        to check the validity of the value
        """
        return True

    def setValue(self, value):
        self.check(value)
        if self.scope == "global":
            self.setGlobal(value)
        elif self.scope == "project":
            self.setProject(value)
        self.valueChanged.emit()

    def getValue(self):
        if self.scope == "global":
            return self.getGlobal()
        elif self.scope == "project":
            return self.getProject()

    def setValueOnWidgetUpdateSignal(self):
        if self.widget is None:
            return
        eval("self.widget.%s.connect(self.setValueFromWidget)" % self.signal)

    def setWidgetFromValue(self):
        if self.widget is None:
            return
        settingValue = self.getValue()
        self.widgetSetMethod(settingValue)

    def setValueFromWidget(self, dummy=None):
        if self.widget is None:
            return
        widgetValue = self.widgetGetMethod()
        self.setValue(widgetValue)
