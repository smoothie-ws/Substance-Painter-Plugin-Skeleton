import json
import substance_painter as sp

from .plugin import Path, Plugin
from .plugin import QtWidgets, QmlView, QtCore


class View(QmlView):
    def __init__(self, path: str):
        super().__init__("Plugin")
        self.widget = None
        
        def cb(container: QtWidgets.QWidget):
            container.setWindowTitle("Python Plugin")
            self.widget = sp.ui.add_dock_widget(container)

        self.load(path, cb)
        
    @QtCore.Slot(result=str)
    def getPluginPath(self):
        return Path.plugin
    
    @QtCore.Slot(result=str)
    def getPluginVersion(self):
        return Plugin.version
    
    @QtCore.Slot(result=str)
    def getPluginSettings(self):
        return json.dumps(Plugin.settings)
