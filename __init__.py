# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AusMap
                                 A QGIS plugin
 AusMap is the essential plugin for Australian QGIS users, providing easy access to free Government Datasets and other web services.
                             -------------------
        begin                : 2017-09-10
        copyright            : (C) 2017 by Daniel Knott
        email                : daniel.knott@watermodelling.com.au
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
    """Load AusMap class from file AusMap.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .aus_map import AusMap
    return AusMap(iface)
