from handwriting_sample.base import HandwritingDataBase


class ReaderException(Exception, HandwritingDataBase):
    """ Base class for TransformerException """

    def __init__(self, message):
        super(ReaderException, self).__init__(message)
        self.log(message)


class HTMLPointerNotAllowedException(Exception, ReaderException):
    """ Base class for TransformerException """

    def __init__(self, message):
        super(HTMLPointerNotAllowedException, self).__init__(message)