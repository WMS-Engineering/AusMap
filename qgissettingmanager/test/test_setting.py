# -----------------------------------------------------------
#
# QGIS Setting Manager
# Copyright (C) 2016 Denis Rouzaud
#
# -----------------------------------------------------------
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
# ---------------------------------------------------------------------

import qgis
from qgis.testing import unittest

import nose2

from .my_settings import MySettings


class TestSetting(unittest.TestCase):
    def test_settings(self):
        for s_name in MySettings().settings_cfg.keys():
            yield self.check_setting, s_name

    def check_setting(self, name):
        setting_ = MySettings().settings_cfg[name]

        # clean just in case
        MySettings().remove(name)

        # default
        self.assertEqual( MySettings().value(name), setting_['default'])

        # set value
        MySettings().set_value(name, setting_['new_value'])
        self.assertEqual(MySettings().value(name), setting_['new_value'])

        # remove setting
        MySettings().remove(name)
        self.assertEqual(MySettings().value(name), setting_['default'])



if __name__ == '__main__':
    nose2.main()
