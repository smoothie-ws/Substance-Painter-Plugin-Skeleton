import json

from .painter import UI, Plugin
from .painter.qml import QtWidgets, QmlView, QtCore


class MainView(QmlView):
    "Example of the qml controller class"
    
    def __init__(self, path: str) -> None:
        super().__init__("Plugin")
        
        def cb(container: QtWidgets.QWidget):
            dock = UI.add_dock(container)
            dock.setWindowTitle("Python Plugin")

        self.load(path, cb)
        
    @QtCore.Slot(result=str)
    def getPluginVersion(self) -> str:
        return Plugin.version
