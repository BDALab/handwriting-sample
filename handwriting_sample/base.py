import os
import time
from datetime import datetime
from handwriting_sample.config import load_configuration


def log(text, topic, be_verbose=False, is_verbose=False):
    """
    Logs the specified text and topic.
    :param text: a text to log.
    :param topic: a topic to log.
    :param be_verbose: True if logging should be verbose.
    :param is_verbose: True if the specified text to log is verbose.
    """
    if not is_verbose or (be_verbose and is_verbose):
        print("{} - {} - {} - {}".format(
            datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
            os.getppid(),
            topic,
            text
        ))


class Base(object):
    """Base class."""

    # Default column names
    AX_X = 'x'
    AX_Y = 'y'
    TIME = 'time'
    PEN_STATUS = 'pen_status'
    AZIMUTH = 'azimuth'
    TILT = 'tilt'
    PRESSURE = 'pressure'

    # Load configuration
    sample_configuration = load_configuration("sample_config.json")

    # Setup column names
    COLUMN_NAMES = sample_configuration.get("column_names", None)

    # Setup date formant
    DATE_FORMAT = sample_configuration.get("date_format", None)

    def log(self, text, be_verbose=False, is_verbose=False):
        """
        Logs the specified text.
        :param text: a text to log.
        :param be_verbose: True if logging should be verbose.
        :param is_verbose: True if the specified text to log is verbose.
        """
        log(text, self.__class__.__name__, be_verbose, is_verbose)
