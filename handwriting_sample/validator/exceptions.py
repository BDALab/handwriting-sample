from handwriting_sample.base import HandwritingDataBase


class ValidatorException(Exception, HandwritingDataBase):
    """ Base class for ValidatorException """

    def __init__(self, message):
        super(ValidatorException, self).__init__(message)
        self.log(message)


class PenStatusException(ValidatorException):

    def __init__(self, value, index):
        self.message = f"Pen status column got and unexpected value on input: {value} on index {index}"

        super(PenStatusException, self).__init__(self.message)