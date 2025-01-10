import datetime

PLUGIN_NAME = "AusMap"

QLR_URL = (
    "https://raw.githubusercontent.com/WMS-Engineering/AusMap/main/ausmap.qlr"
)

ABOUT_FILE_URL = (
    "https://wmseng.com.au/"  # TODO: Add tool description on WMS website
)

FILE_MAX_AGE = datetime.timedelta(hours=72)
