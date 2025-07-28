from .bridge import Log, Path, SPPlugin
from .controller import View


class Plugin(SPPlugin):
    @classmethod
    def start(cls, path):
        super().start(path, "Python Plugin")
        
    @classmethod
    def on_start(cls):
        dock_view = View(Path.asset("ui", "View.qml"))
        Plugin.widgets.append(dock_view)
    
    @classmethod
    def on_project_opened(cls):
        Log.info("Project opened")

    @classmethod
    def on_project_about_to_close(cls):
        Log.info("Project about to close")
