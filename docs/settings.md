---
title: Settings
layout: page
nav_order: 4
permalink: /settings/
---

# Settings

The AusMap plugin can be extended with additional map layers saved in a Layer Definition File (QLR). The map layers in this file will be added to the AusMap menu and therefore easily accessible.  

The QLR file must match the AusMap menu layout, meaning that the map layers must be grouped into one or more categories.  

See the example below.

## Example

The additional layers 1, 2 and 3 are grouped into two categories.

![Grouped map layers](/assets/images/grouped-layers.png)

Save the layers in a QLR file by selecting the groups, right-clicking, and choosing **Export** > **Save as Layer Definition File**.

![Save QLR](/assets/images/save-qlr.png)

Navigate to the AusMap page in the options dialog (**Settings** > **Options** > **AusMap**), select the QLR file from your local machine and click **OK**.  

![AusMap options dialog](/assets/images/options-dialog.png)

The additional map layers will now appear in their respective groups inside the AusMap menu.  

![Custom layers in menu](/assets/images/new_layers_in_menu.png)

To remove the layers from the menu, go back to the options dialog, delete the file path and save.

