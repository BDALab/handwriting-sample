import os
import time
from datetime import datetime


def log(text, topic, be_verbose=False, is_verbose=False):
    """
    Logs the specified text and topic.

    More info:
    ``be_verbose`` is True if logging should be verbose
    ``is_verbose`` is True if the specified text to log is verbose

    :param text: a text to log
    :type text: str
    :param topic: a topic to log
    :type topic: str
    :param be_verbose: verbosity of the logging, defaults to False
    :type be_verbose: bool, optional
    :param is_verbose: verbosity of the text, defaults to False
    :type is_verbose: bool, optional
    :return: None
    :rtype: None type
    """
    if not is_verbose or (be_verbose and is_verbose):
        print(
            f"{datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')} - "
            f"{os.getppid()} - "
            f"{topic} - "
            f"{text}")
