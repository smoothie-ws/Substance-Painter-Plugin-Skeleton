from .painter import Log, Plugin, QmlView
from .controller import MainView


class PythonPlugin(Plugin):
    "Your Python plugin"
    
    dock_view: MainView = None
    
    @classmethod
    def on_start(cls) -> None:
        PythonPlugin.dock_view = MainView(QmlView.view_path("View.qml"))
    
    @classmethod
    def on_project_opened(cls) -> None:
        Log.info("Project opened")

    @classmethod
    def on_project_about_to_close(cls) -> None:
        Log.info("Project about to close")
