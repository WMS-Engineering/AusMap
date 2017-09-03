# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ausmap
                                 A QGIS plugin
 Easy access to WMS from ausmap
                             -------------------
        begin                : 2015-05-01
        copyright            : (C) 2016 by Septima P/S
        email                : kontakt@septima.dk
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load ausmap class from file ausmap.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .ausmap import ausmap
    return ausmap(iface)
