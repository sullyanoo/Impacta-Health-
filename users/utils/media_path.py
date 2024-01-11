import logging
import os
from uuid import uuid4

from logs.config import SetUpLogging

SetUpLogging()


def set_avatar_path(instance, filename):
    try:
        filename = filename[-10:]
        result = os.path.join(f"users/avatars/{str(uuid4())}-{instance.user.username}-{filename}")

        return result.lower().replace(" ", "")
    except Exception as msg:
        logging.error(msg, exc_info=True)
        raise msg
