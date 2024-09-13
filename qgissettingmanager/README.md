[![Build Status](https://travis-ci.org/3nids/qgissettingmanager.svg?branch=master)](https://travis-ci.org/3nids/qgissettingmanager)

## About

Easily manage the settings in your [QGIS](http://www.qgis.org) plugin.

This module can:

* manage **different types of settings** (bool, string, color, integer, double, stringlist)
* **read and write settings** both in QGIS application or in the QGIS project
* automatically **set widgets** of a dialog according to their **corresponding setting**
* automatically **write settings from their corresponding widgets**


## The main setting class

All your settings shall be saved in a single class, which will subclass SettingManager.

```python
from qgissettingmanager import *

class MySettings(SettingManager):
    def __init__(self):
        SettingManager.__init__(self, my_plugin_name)
        self.add_setting( Bool("my_setting", Scope.Global, True) )
```
    
You may add as many settings as you want using `add_setting` method:

```python
add_setting( SettingClass( name, scope, default_value, options={} ) )
```

* `SettingClass`: `Bool`, `String`, `Color`, `Integer`, `Double` or `Stringlist`
* `name`: the name of the setting
* `scope`: `Scope.Global` or `Scope.Project`
* `default_value`: the default value of the setting (type must correspond)
* `options`: a dictionary of options for widgets (see [possible widgets](#possiblewidgets))

### Access the settings

Instantiate your settings class in your current class:

```python
import MySettings
self.settings = MySettings()
```

The settings are easily accessed using the `value` and `setValue` methods:

```python
myVariable = self.settings.value("myVariable")
self.settings.set_value("myVariable", False)
```

### Remove settings

Settings can be removed from registry (local or project wise) using `MySettings().remove('my_setting')`.


## Match settings with widgets of a dialog

### Quick start

You can associate a setting to a defined widget in a dialog (or a dockable window). The first condition is to **name the widget as the setting name**.
Then, your dialog class shall subclass the `SettingDialog` class:

```python
class MyDialog(QDialog, Ui_myDialog, SettingDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.settings = MySettings()
        SettingDialog.__init__(self, self.settings)
```

Hence, when the dialog is shown, all widgets which are named according to a  setting will be set to the corresponding value. On dialog acceptance, the settings will be set according to the value read from their widget.

To control which setting has been associated to a widget, you can print `self.widget_list()`.

### Settings' update behavior

You can have a different behavior using `SettingDialog` parameters:

```python
SettingDialog(settingManager, mode=UpdateMode.DialogAccept)
```

`mode` can take the following values:

* `UpdateMode.NoUpdate`: settings values won't be updated;
* `UpdateMode.DialogAccept`: settings values are set when the dialog is accepted _(default)_;
* `UpdateMode.WidgetUpdate`: settings are set as soon as the widget is modified.

### Check something before updating the settings

You can override the `SettingDialog.before_accept_dialog()` method to check your settings.
Settings will be saved only if the method returns `True`.

### Using showEvent

Be warned that `SettingDialog` implements `showEvent` method. Therefore, if you redefine it in your dialog class, you have to write:

```python
def showEvent(self, e):
    settingDialog.showEvent(self, e)
    # do your own stuff
```

<a name="possiblewidgets"/>
### Possible widgets

The widgets are automatically detected by the manager. If the type of widget is not handled, an error is raised.

**Strings**

* `QLineEdit`
* `QComboBox` (setting can be defined as the current item text or [data](http://qt-project.org/doc/qt-4.8/qcombobox.html#itemData): specify option `comboMode` as `data` (default) or `text`)
* `QButtonGroup` (the setting is set as the checked widget text in the button group)
* `QgsMapLayerComboBox` uses layer ID for the setting value

**Booleans**

* `QCheckBox`
* Any checkable widget (groupbox, etc.)

**Colors**

* Native QGIS widgets (QgsColorButton) or any widget (label or pushbutton are recommended). For standard Qt Widgets, QGIS [color button](http://qgis.org/api/classQgsColorButton.html)) will be used. Use options `allowAlpha` (boolean) to allow transparent colors and `dialogTitle` to set the dialog title.

**Integers**

* `QLineEdit`
* `QSpinBox`
* `QSlider`
* `QComboBox` (setting is set as the combo box index)

**Doubles**

* `QLineEdit`
* `QDoubleSpinBox`

**Stringlist**

* `QListWidget` (checks items having their _text_ in the list)
* `QButtonGroup` (checks items having their _name_ in the list)

New types of widget are easily added, if one is missing, do not hesitate to [ask](https://github.com/3nids/qgissettingmanager/issues)!


## Using git submodules

To use this module, you can easily copy the files and put them in your project.
A more elegant way is to use [git submodule](http://git-scm.com/book/en/Git-Tools-Submodules). Hence, you can keep up with latest improvements. In you plugin directory, do

```
git submodule add https://github.com/3nids/qgissettingmanager.git
```

A folder _qgissettingmanager_ will be added to your plugin directory. However, git only references the module, and you can `git pull` in this folder to get the last changes.
