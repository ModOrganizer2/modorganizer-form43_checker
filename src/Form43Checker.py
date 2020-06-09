from pathlib import Path
import sys

from PyQt5.QtCore import QCoreApplication

if "mobase" not in sys.modules:
    import mock_mobase as mobase

class Form43Checker(mobase.IPluginDiagnose):

    def __init__(self):
        super(Form43Checker, self).__init__()
        self.__organizer = None

    def init(self, organizer):
        self.__organizer = organizer
        return True

    def name(self):
        return "Form 43 Plugin Checker"

    def author(self):
        return "AnyOldName3"

    def description(self):
        return self.__tr("Checks plugins (.ESM/.ESP files) to see if any are lower than Form 44 (Skyrim SE).")

    def version(self):
        return mobase.VersionInfo(1, 2, 0, mobase.ReleaseType.prealpha)

    def isActive(self):
        return (self.__organizer.managedGame().gameName() == "Skyrim Special Edition" and
                self.__organizer.pluginSetting(self.name(), "enabled") is True)

    def settings(self):
        return [
            mobase.PluginSetting("enabled", self.__tr("Enable plugin"), True)
        ]

    def activeProblems(self):
        if self.__scanPlugins():
            return [0]
        else:
            return []

    def shortDescription(self, key):
        return self.__tr("Form 43 (or lower) plugin detected")

    def fullDescription(self, key):
        pluginList = self.__listPlugins()
        pluginList = [Path(absolutePath).name for absolutePath in pluginList]
        pluginListString = "<br><br>•  " + ("<br>•  ".join(pluginList))
        outputString = self.__tr("You have one or more plugins that are not form 44. They are:{0}").format(pluginListString)
        outputString += "<br><br>"
        outputString += self.__tr("Form 43 (or lower) plugins are modules that were made for Skyrim LE (Oldrim) and have not been "
                                  "properly ported to Skyrim Special Edition, which uses form 44 plugins. This usually results in "
                                  "parts of the mod not working correctly."
                                  "<br><br>"
                                  "To be converted, these plugins simply need to be opened and saved with the SSE Creation Kit "
                                  "but their presence can be an indication that a mod was not properly ported to SSE and so "
                                  "can potentially have additional issues." 
                                  "<br><br>"
                                  "Online guides can have more information on how to correctly convert mods for Skyrim SE.<br>")
        return outputString

    def hasGuidedFix(self, key):
        return False

    def startGuidedFix(self, key):
        # Maybe we could use xEdit or something to resave the file?
        pass

    def __tr(self, str):
        return QCoreApplication.translate("Form43Checker", str)

    def __testFile(self, path):
        version = self.__getForm(path)
        if isinstance(version, int):
            return version < 44
        else:
            return None

    def __getForm(self, file):
        path = Path(file)
        if path.is_file():
            with path.open(mode='rb') as file:
                file.seek(20)
                return int.from_bytes(file.read(2), byteorder='little')
        else:
            return "invalid"

    def __listInvalidFiles(self):
        for file in self.__organizer.findFiles("", "*.es[pm]"):
            if self.__testFile(file):
                yield file

    def __scanPlugins(self):
        if self.__organizer.managedGame().gameName() != "Skyrim Special Edition":
            return False

        # Return True if there is at least one invalid file:
        return next(self.__listInvalidFiles(), False)

    def __listPlugins(self):
        return ["{} (form {})".format(file, self.__getForm(file)) for file in self.__listInvalidFiles()]


def createPlugin():
    return Form43Checker()