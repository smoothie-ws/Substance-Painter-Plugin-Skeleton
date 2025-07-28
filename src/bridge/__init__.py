import json
import substance_painter as sp

from .log import Log
from .path import Path
from .resource import Resource
from .qml import QmlView, QmlWindow
from .project_settings import ProjectSettings


class SPPlugin:
    files = []
    settings = {}
    version = "0.0.1a"
    
    widgets: list = []
    
    @classmethod
    def start(cls, path: str, name: str):
        Log.channel = name
        Path.plugin = path
        Path.settings = Path.join(Path.plugin, "plugin.json")
        Path.documents = sp.js.evaluate("alg.documents_directory")
        
        try:
            data = json.loads(Path.read(Path.settings, {}))
            cls.files = data.get("files", [])
            cls.settings = data.get("settings", {})
            cls.version = data.get("version", "0.0.1a")
            
            connections = {
                sp.event.ProjectOpened: lambda _: cls.on_project_opened(),
                sp.event.ProjectAboutToClose: lambda _: cls.on_project_about_to_close()
            }
            for event, callback in connections.items():
                sp.event.DISPATCHER.connect_strong(event, callback)
                
            cls.on_start()
            Log.warning(f'Plugin started (version {cls.version})')
            
            if sp.project.is_open():
                cls.on_project_opened()
        except:
            cls.on_close()
            Log.fatal()

    @classmethod
    def close(cls):
        cls.save()
        cls.on_close()
        for widget in cls.widgets:
            sp.ui.delete_ui_element(widget)
        Log.warning("Plugin closed")
    
    @classmethod
    def push_file(cls, path: str):
        if not path in cls.files:
            cls.files.append(path)
            cls.save()

    @classmethod
    def save(cls):
        Path.write(Path.settings, json.dumps({
            "version": cls.version,
            "files": cls.files,
            "settings": cls.settings
        }, indent=4, ensure_ascii=False))
        
    # to override
    
    @classmethod
    def on_start(cls):
        pass
    
    @classmethod
    def on_close(cls):
        pass
        
    @classmethod
    def on_project_opened(cls):
        pass
    
    @classmethod
    def on_project_about_to_close(cls):
        pass
    