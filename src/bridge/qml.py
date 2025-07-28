import json
import substance_painter as sp

# qt5 vs qt6 check
if sp.application.version_info() < (10, 1, 0):
    from PySide2 import QtQuickWidgets, QtWidgets, QtCore, QtGui
else:
    from PySide6 import QtQuickWidgets, QtWidgets, QtCore, QtGui

from .log import Log
from .path import Path


class QmlView(QtCore.QObject):
    "Bridge class between Python and QML"

    def __init__(self, name: str = "Plugin", path: str = None):
        super().__init__()
        self.name = name
        self.view = QtQuickWidgets.QQuickWidget()
        self.view.setResizeMode(QtQuickWidgets.QQuickWidget.SizeRootObjectToView)
        
        if path is not None:
            self.load(path)
    
    def load(self, path: str, callback = None):
        def start(status: QtQuickWidgets.QQuickWidget.Status):
            if status == QtQuickWidgets.QQuickWidget.Ready:
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
            raise Exception(f'File {path} does not exist')

    # common slots
    @QtCore.Slot(str, result=str)
    def js(self, code: str):
        try:
            return json.dumps(sp.js.evaluate(code))
        except Exception as e:
            Log.error(f'Failed to evaluate js code: {str(e)}')
            Log.info(code)
    
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
    opened = QtCore.Signal()
    closed = QtCore.Signal()
    
    def __init__(self, title: str, icon: QtGui.QIcon = None, name: str = "Plugin", path: str = None):
        self.window = QtWidgets.QMainWindow(
            parent=sp.ui.get_main_window(),
            flags=QtCore.Qt.WindowType.Window | 
                QtCore.Qt.WindowType.CustomizeWindowHint | 
                QtCore.Qt.WindowType.WindowTitleHint | 
                QtCore.Qt.WindowType.WindowCloseButtonHint
        )
        self.window.setWindowIcon(icon)
        self.window.setWindowTitle(title)
        self.window.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        super().__init__(name, path)
        
        def on_closed(event: QtGui.QCloseEvent):
            self.closed.emit()
            event.accept()
            
        self.window.closeEvent = on_closed
    
    def load(self, path: str, callback = None):
        def cb(container: QtWidgets.QWidget):
            self.window.setCentralWidget(container)
            if callback is not None:
                callback(container)
        super().load(path, cb)

    def open(self):
        screen_geometry = QtWidgets.QApplication.primaryScreen().availableGeometry()
        x = (screen_geometry.width() - self.window.width()) // 2
        y = (screen_geometry.height() - self.window.height()) // 2
        self.window.move(x, y)
        self.window.show()
        self.opened.emit()

    @QtCore.Slot()
    def close(self):
        self.window.close()
        self.closed.emit()


class QmlDialog(QmlWindow):
    def close(self):
        super().close()
        self.on_cancelled()

    @QtCore.Slot(str)
    def confirm(self, data: str):
        self.window.close()
        self.on_confirmed(data)

    # to override
    
    def on_confirmed(self, data: str):
        pass

    def on_cancelled(self):
        pass
