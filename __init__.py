from .ausmap import AusMap


def classFactory(iface):
    """
    Initialize the plugin
    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    return AusMap(iface)
