import json
import substance_painter as sp

from abc import abstractmethod
from time import localtime, strftime

from .log import Log
from .path import Path
from .plugin import Plugin
from .ui import UI, QtQuickWidgets, QtWidgets, QtCore, QtGui


class QmlView(QtCore.QObject):
    "Bridge class between Python and QML"

    @classmethod
    def view_path(cls, path: str):
        return Path.join(Path.plugin, "view", path)
    
    def __init__(self, name: str = "Plugin", path: str = None):
        super().__init__()
        self.name = name
        self.view = QtQuickWidgets.QQuickWidget()
        self.view.setResizeMode(QtQuickWidgets.QQuickWidget.ResizeMode.SizeRootObjectToView)
        
        if path is not None:
            self.load(path)
    
    def load(self, path: str, callback = None):
        def start(status: QtQuickWidgets.QQuickWidget.Status):
            if status == QtQuickWidgets.QQuickWidget.Status.Ready:
                if callback is not None:
                    callback(self.view)
            else:
                Log.error(str([e.toString() for e in self.view.errors()]))
            
        def on_warnings(warnings):
            for w in warnings:
                Log.error(w.toString())
                
        if Path.exists(path):
            engine = self.view.engine()
            engine.warnings.connect(on_warnings)
            engine.rootContext().setContextProperty(self.name, self)
            # load view
            self.view.statusChanged.connect(start)
            self.view.setSource(QtCore.QUrl.fromLocalFile(path))
        else:
            Log.error(f'File {path} does not exist')

    # common slots
    @QtCore.Slot(str, result=str)
    def js(self, code: str):
        try:
            res = sp.js.evaluate(code)
        except:
            res = None
        return json.dumps(res)
    
    @QtCore.Slot(result=str)
    def time(self) -> str:
        return strftime("%H:%M:%S", localtime())
    
    @QtCore.Slot(str, result=str)
    def asset(self, path: str) -> str:
        return f'file:{Path.asset(path)}'
    
    @QtCore.Slot(str, result=bool)
    def pathExists(self, path: str) -> bool:
        return Path.exists(path)
        
    @QtCore.Slot(str)
    def info(self, msg: str):
        Log.info(msg)
    
    @QtCore.Slot(str)
    def warning(self, msg: str):
        Log.warning(msg)

    @QtCore.Slot(str)
    def error(self, msg: str):
        Log.error(msg)
        
    
class QmlWindow(QmlView):
    def __init__(self, title: str, icon: QtGui.QIcon = None, name: str = "Plugin", path: str = None):
        self.window = UI.add_window(QtWidgets.QMainWindow(
            parent=sp.ui.get_main_window(),
            flags=QtCore.Qt.WindowType.Window | 
                QtCore.Qt.WindowType.CustomizeWindowHint | 
                QtCore.Qt.WindowType.WindowTitleHint | 
                QtCore.Qt.WindowType.WindowCloseButtonHint
        ))
        super().__init__(name, path)
        
        def on_closed(event: QtGui.QCloseEvent):
            self.closed.emit()
            event.accept()
            
        self.window.closeEvent = on_closed
        self.window.setWindowIcon(icon)
        self.window.setWindowTitle(title)
        self.window.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        
    opened = QtCore.Signal()
    closed = QtCore.Signal()
    
    def load(self, path: str, callback = None):
        def cb(container: QtWidgets.QWidget):
            self.window.setCentralWidget(container)
            if callback is not None:
                callback(container)
        super().load(path, cb)

    def show(self):
        screen_geometry = QtWidgets.QApplication.primaryScreen().availableGeometry()
        self.window.move(
            (screen_geometry.width() - self.window.width()) // 2, 
            (screen_geometry.height() - self.window.height()) // 2
        )
        self.window.show()
        
    def open(self):
        self.show()
        self.opened.emit()

    @QtCore.Slot()
    def close(self):
        self.window.close()


class QmlDialog(QmlWindow):
    def close(self):
        super().close()
        self.on_cancelled()

    @QtCore.Slot(str)
    def confirm(self, data: str):
        self.window.close()
        self.on_confirmed(data)

    # to override
    
    @abstractmethod
    def on_confirmed(self, data: str): ...

    @abstractmethod
    def on_cancelled(self): ...
