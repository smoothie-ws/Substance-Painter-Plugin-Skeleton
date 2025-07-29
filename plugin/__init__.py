from .painter import Log, Plugin
from .controller import DockView


class PythonPlugin(Plugin):
    "Your Python plugin"
    
    dock_view: DockView = None
    
    @classmethod
    def on_start(cls) -> None:
        PythonPlugin.dock_view: DockView = DockView.from_plugin_file("View.qml")
    
    @classmethod
    def on_project_opened(cls) -> None:
        Log.info("Project opened")

    @classmethod
    def on_project_about_to_close(cls) -> None:
        Log.info("Project about to close")
