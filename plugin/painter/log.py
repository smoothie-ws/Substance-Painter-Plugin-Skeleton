import traceback
import substance_painter as sp


class Log:
    channel: str = "Plugin"

    @staticmethod
    def info(msg: str) -> None:
        sp.logging.log(sp.logging.INFO, Log.channel, msg)
    
    @staticmethod
    def error(msg: str) -> None:
        sp.logging.log(sp.logging.ERROR, Log.channel, msg)
    
    @staticmethod
    def warning(msg: str) -> None:
        sp.logging.log(sp.logging.WARNING, Log.channel, msg)

    @staticmethod
    def fatal() -> None:
        Log.error(traceback.format_exc())
        