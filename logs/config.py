from logging import basicConfig, DEBUG, handlers, StreamHandler, WARNING

from decouple import config


class SetUpLogging:
    def __init__(self) -> object:
        """
        Initialize log manager based on production or development mode
        """
        PRODUCTION_FILE_HANDLER = handlers.RotatingFileHandler(
            "logs/production.log",
            mode="a",
            maxBytes=10485760,
            backupCount=20,
        )
        PRODUCTION_FILE_HANDLER.setLevel(WARNING)

        STREAM_HANDLER = StreamHandler()
        STREAM_HANDLER.setLevel(DEBUG)

        DEVELOPMENT_MODE = {
            "True": STREAM_HANDLER,
            "False": PRODUCTION_FILE_HANDLER,
        }

        DEBUG_STATEMENT = config("DEBUG")
        handler = DEVELOPMENT_MODE.get(DEBUG_STATEMENT)

        basicConfig(
            format="%(levelname)s: [%(asctime)s] - %(pathname)s:%(lineno)d - %(message)s",
            handlers=[handler],
        )
