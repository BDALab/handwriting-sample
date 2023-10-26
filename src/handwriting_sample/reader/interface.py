from handwriting_sample.base import LoggableObject
from handwriting_sample.reader.readers import (
    JSONFileReader,
    SVCFileReader,
    ListReader,
    NumpyArrayReader,
    PandasDataFrameReader,
    HTMLPointerEventReader
)


class HandwritingSampleReader(LoggableObject):
    """Class implementing handwriting data reader"""

    # --------------- #
    # Reading methods #
    # --------------- #

    @classmethod
    def read_from_json(cls, path, columns, verbose=False):
        """
        Reads handwriting data and meta data from a JSON file.

        :param path: path to a JSON file
        :type path: str
        :param columns: handwriting variables to be present in the data
        :type columns: list
        :param verbose: verbosity of the logging, defaults to False
        :type verbose: bool, optional
        :return: data and meta data
        :rtype: tuple
        """
        return JSONFileReader.read(path, verbose=verbose)

    @classmethod
    def read_from_svc(cls, path, columns, verbose=False):
        """
        Reads handwriting data and meta data from an SVC file.

        :param path: path to an SVC file
        :type path: str
        :param columns: handwriting variables to be present in the data
        :type columns: list
        :param verbose: verbosity of the logging, defaults to False
        :type verbose: bool, optional
        :return: data and meta data
        :rtype: tuple
        """
        return SVCFileReader.read(path, columns, verbose=verbose)

    @classmethod
    def read_from_list(cls, data, columns, verbose=False):
        """
        Reads handwriting data and meta data from a list.

        :param data: data representing handwriting sample
        :type data: list
        :param columns: handwriting variables to be present in the data
        :type columns: list
        :param verbose: verbosity of the logging, defaults to False
        :type verbose: bool, optional
        :return: data and meta data
        :rtype: tuple
        """
        return ListReader.read(data, columns, verbose=verbose)

    @classmethod
    def read_from_numpy_array(cls, data, columns, verbose=False):
        """
        Reads handwriting data and meta data from a numpy array.

        :param data: data representing handwriting sample
        :type data: np.ndarray
        :param columns: handwriting variables to be present in the data
        :type columns: list
        :param verbose: verbosity of the logging, defaults to False
        :type verbose: bool, optional
        :return: data and meta data
        :rtype: tuple
        """
        return NumpyArrayReader.read(data, columns, verbose=verbose)

    @classmethod
    def read_from_pandas_dataframe(cls, data, columns, verbose=False):
        """
        Reads handwriting data and meta data from a pandas DataFrame.

        :param data: data representing handwriting sample
        :type data: pd.DataFrame
        :param columns: handwriting variables to be present in the data
        :type columns: list
        :param verbose: verbosity of the logging, defaults to False
        :type verbose: bool, optional
        :return: data and meta data
        :rtype: tuple
        """
        return PandasDataFrameReader.read(data, verbose=verbose)

    @classmethod
    def read_from_html_pointer_event(cls, data, columns, verbose=False):
        """
        Reads handwriting data and meta data from a list.

        :param data: data representing handwriting sample
        :type data: dict
        :param columns: handwriting variables to be present in the data
        :type columns: list
        :param verbose: verbosity of the logging, defaults to False
        :type verbose: bool, optional
        :return: data and meta data
        :rtype: tuple
        """
        return HTMLPointerEventReader.read(data, verbose=verbose)
