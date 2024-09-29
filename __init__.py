"""
This script initializes the plugin, making it known to QGIS.
"""
from .ausmap import AusMap
def classFactory(iface):
    """
    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    from .ausmap import AusMap
    return AusMap(iface)
