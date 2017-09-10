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

from PyQt4.QtCore import QSettings
from PyQt4.QtGui import QCheckBox
from qgis.core import QgsProject

from ..setting import Setting


class Bool(Setting):

    def __init__(self, pluginName, name, scope, defaultValue, options={}):

        setGlobal = lambda(value): QSettings(pluginName, pluginName).setValue(name, value)
        setProject = lambda(value): QgsProject.instance().writeEntryBool(pluginName, name, value)
        getGlobal = lambda: QSettings(pluginName, pluginName).value(name, defaultValue, type=bool)
        getProject = lambda: QgsProject.instance().readBoolEntry(pluginName, name, defaultValue)[0]

        Setting.__init__(self, pluginName, name, scope, defaultValue, options,
                         setGlobal, setProject, getGlobal, getProject)

    def check(self, value):
        if type(value) != bool:
            raise NameError("Setting %s must be a boolean." % self.name)

    def setWidget(self, widget):
        if type(widget) == QCheckBox or (hasattr(widget, "isCheckable") and widget.isCheckable()):
            self.signal = "clicked"
            self.widgetSetMethod = widget.setChecked
            self.widgetGetMethod = widget.isChecked
        else:
            print type(widget)
            raise NameError("SettingManager does not handle %s widgets for booleans for the moment (setting: %s)" %
                            (type(widget), self.name))
        self.widget = widget
