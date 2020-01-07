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
        return self.__tr("Checks plugins (.ESM/.ESP files) to see if any are Form 43 (Skyrim LE).")

    def version(self):
        return mobase.VersionInfo(1, 0, 0, mobase.ReleaseType.prealpha)

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
        return self.__tr("Form 43 plugin detected")

    def fullDescription(self, key):
        pluginList = self.__listPlugins()
        pluginList = [Path(absolutePath).name for absolutePath in pluginList]
        pluginListString = "\n• " + ("\n• ".join(pluginList))
        return self.__tr("You have one or more Form 43 plugins. They are:{0}").format(pluginListString)

    def hasGuidedFix(self, key):
        return False

    def startGuidedFix(self, key):
        # Maybe we could use xEdit or something to resave the file?
        pass

    def __tr(self, str):
        return QCoreApplication.translate("Form43Checker", str)

    def __testFile(self, path):
        path = Path(path)
        if path.is_file():
            with path.open(mode='rb') as file:
                file.seek(20)
                version = file.read(2)
                return version == b"\x2b\x00"
        else:
            return None

    def __scanPlugins(self):
        if self.__organizer.managedGame().gameName() != "Skyrim Special Edition":
            return False

        def isPluginFile(name):
            extension = Path(name).suffix
            extension = extension.lower()
            return extension == ".esp" or extension == ".esm"

        fileList = self.__organizer.findFiles("", isPluginFile)

        for file in fileList:
            if self.__testFile(file):
                return True

        return False

    def __listPlugins(self):
        def isPluginFile(name):
            extension = Path(name).suffix
            extension = extension.lower()
            return extension == ".esp" or extension == ".esm"

        fileList = self.__organizer.findFiles("", isPluginFile)

        return [file for file in fileList if self.__testFile(file)]


def createPlugin():
    return Form43Checker()