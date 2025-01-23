# AusMap

<img src="https://github.com/WMS-Engineering/AusMap/blob/main/img/icon.png?raw=true" alt="AusMap logo" height="100">

AusMap is a QGIS plugin for visualising publicly available Australian geographic data. AusMap gives quick access to a variety of feature sets and map layers provided by Geoscience Australia, the Google Maps Platform and OpenStreetMap. Selecting a desired layer from the AusMap menu will add it to the map canvas with styling and labelling applied. The layers are provided via WMS, WFS, WMTS and XYZ services, which all require an active internet connection.

## Features

- Access to a wide range of Australian geographic data from Geoscience Australia
- Seamless integration with QGIS, allowing easy search and display of map layers
- Extend the plugin with a custom Layer Definition File (.QLR)

## Installation

### Requirements

- QGIS version 3.18 or higher
- Internet access for fetching online map layer web services

### Installation through QGIS

1. Open QGIS.
2. Navigate to `Plugins` > `Manage and Install Plugins`.
3. Search for *AusMap*.
4. Click the `Install` button.

### Installation through GitHub

1. Download the ZIP file from this repository.
2. In QGIS, navigate to `Plugins` > `Manage and Install Plugins`.
3. Click `Install from ZIP` and select the downloaded plugin file.

## Contributing

Please report any bugs or feature requests by creating an issue in this GitHub repository.

## Credits and License

AusMap was developed and is maintained by WMS Engineering and is licensed under the GNU General Public License (GPL) v3.0 or later. You are free to use, modify, and distribute this plugin under the terms of the GNU GPL as published by the Free Software Foundation. This plugin is distributed in the hope that it will be useful, but without any warranty. See the [GNU GPL](https://www.gnu.org/licenses/) for more details.
The design and functionality of AusMap draw inspiration from the [Dataforsyningen QGIS plugin](https://github.com/SDFIdk/Qgis-dataforsyningen).
For more detailed instructions and usage guidelines, refer to the [User Manual](https://wms-engineering.github.io/AusMap/).
