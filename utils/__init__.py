from qgis.core import QgsMessageLog


def log_message(message):
    QgsMessageLog.logMessage(message, 'AusMap plugin')