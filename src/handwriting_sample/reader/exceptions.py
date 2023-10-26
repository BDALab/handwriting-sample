from handwriting_sample.base import HandwritingDataBase


class ReaderException(Exception, HandwritingDataBase):
    """ Base class for TransformerException """

    def __init__(self, message):
        super(ReaderException, self).__init__(message)
        self.log(message)


class HTMLPointerNotAllowedException(ReaderException):
    """ Base class for TransformerException """

    def __init__(self, message):
        super(HTMLPointerNotAllowedException, self).__init__(message)


class HTMLDataMissingColumn(ReaderException):
    """ Base class for TransformerException """

    def __init__(self, message):
        super(HTMLDataMissingColumn, self).__init__(message)


class HTMLDataMColumnMissingValues(ReaderException):
    """ Base class for TransformerException """

    def __init__(self, message):
        super(HTMLDataMColumnMissingValues, self).__init__(message)
