# About

Easily manage the settings in your [QGIS](http://www.qgis.org) plugin.

This module can:
* manage **different types of settings** (bool, string, color, integer, double, stringlist)
* **read and write settings** in QGIS application or in the QGIS project
* automatically **set widgets from corresponding setting**
* automatically **write settings from widgets of a dialog**


## The main setting class

All your settings will be saved in a single class, which will subclass SettingManager.

```python
from qgissettingmanager import *

class MySettings(SettingManager):
    def __init__(self):
        SettingManager.__init__(self, myPluginName)
        self.addSetting("myVariable", "bool", "global", True)
```
    
You add as many settings as you want using _addSetting_ method:

```python
addSetting(name, settingType, scope, defaultValue, options={})
```

* **name**: the name of the setting
* **settingType**: _bool_, _string_, _color_, _integer_, _double_ or _stringlist_
* **scope**: _global_ or _project_
* **defaultValue**: the default value of the setting (type must corrsepond)
* **options**: a dictionary of options for widgets (see [possible widgets](#possiblewidgets))

## Access the settings

Instantiate your settings class in your current class:

```python
import MySettings
self.settings = MySettings()
```

The settings are easily accessed using the `value` and `setValue` methods:

```python
myVariable = self.settings.value("myVariable")
self.settings.setValue("myVariable", False)
```

## Match settings with widgets of a dialog

### Quick start

You can associate a setting to a defined widget in a dialog (or a dockable window). The first point is to **name the widget as the setting name**.
Then, your dialog class subclasses the `SettingDialog` class:

```python
class MyDialog(QDialog, Ui_myDialog, SettingDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.settings = MySettings()
        SettingDialog.__init__(self, self.settings)
```

Hence, must dialog is shown, all widgets which are named as some setting will be set to the corresponding value. On dialog acceptance, the setting will be set according to their widget.

To control which setting has been associated to a widget, you can write `print self.widgetList()`.

### Settings' update behavior

You can have a different behavior using `SettingDialog` parameters:

```python
SettingDialog(settingManager, setValuesOnDialogAccepted=True, setValueOnWidgetUpdate=False)
```

* setValuesOnDialogAccepted: if `True`, settings values are set when dialog is accepted;
* setValueOnWidgetUpdate: if `True`, settings are set as soon as the widgets is modified.

### Check something before updating the settings

You can override the `SettingDialog.onBeforeAcceptDialog()` method to check your settings.
Settings will be saved only if method returns `True`.

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

* QLineEdit
* QComboBox (setting can be defined as the current item text or [data](http://qt-project.org/doc/qt-4.8/qcombobox.html#itemData): specify option _comboMode_ as _data_ (default) or _text_)
* QButtonGroup (the setting is set as the checked widget text in the button group)

**Booleans**

* QCheckBox
* Any checkable widget (groupbox, etc.)

**Colors**

* Any widget but labels or pushbuttons are recommended (it uses QGIS [color button](http://qgis.org/api/classQgsColorButton.html)). Use option _dialogTitle_ to set the dialog title.

**Integers**

* QLineEdit
* QSpinBox
* QSlider
* QComboBox (setting is set as the combo box index)

**Doubles**

* QLineEdit
* QDoubleSpinBox

**Stringlist**

* QListWidget (checks items having their _text_ in the list)
* QButtonGroup (checks items having their _name_ in the list)

New types of widget are easily added, if one is missing, do not hesitate to [ask](https://github.com/3nids/qgissettingmanager/issues)!



## Using git submodules

To use this module, you can easily copy the files and put them in your project.
A more elegant way is to use [git submodule](http://git-scm.com/book/en/Git-Tools-Submodules). Hence, you can keep up with latest improvements. In you plugin directory, do

```
git submodule add git://github.com/3nids/qgissettingmanager.git
```

A folder _qgissettingmanager_ will be added to your plugin directory. However, git only references the module, and you can `git pull` in this folder to get the last changes.
