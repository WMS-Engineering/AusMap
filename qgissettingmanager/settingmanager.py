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


from types import *

# to print debug info
Debug = False

# possible types
valueTypes = ("string", "double", "integer", "bool", "color", "stringlist")


class SettingManager():
    def __init__(self, pluginName):
        self.pluginName = pluginName
        self.settings = []

    def addSetting(self, name, settingType, scope, defaultValue, options={}):
        if self.setting(name) is not None:
            raise NameError("%s already exist in settings." % name)
        if settingType.lower() not in valueTypes:
            raise NameError("Wrong type %s" % settingType)
        if scope.lower() not in ("global", "project"):
            raise NameError("%s is not a valid scope. Must be project or global." % scope)
        SettingClass = globals()[settingType[0].upper() + settingType[1:].lower()]
        setting = SettingClass(self.pluginName, name, scope, defaultValue, options)
        self.settings.append(setting)

    def setting(self, name):
        for setting in self.settings:
            if setting.name == name:
                return setting
        return None

    def value(self, settingName):
        setting = self.setting(settingName)
        if setting is None:
            raise NameError('%s has no setting %s' % (self.pluginName, settingName))
        return setting.getValue()

    def setValue(self, settingName, value):
        setting = self.setting(settingName)
        if setting is None:
            raise NameError('%s has no setting %s' % (self.pluginName, settingName))
        setting.setValue(value)






