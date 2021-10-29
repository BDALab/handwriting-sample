from base import HandwritingDataBase


class TransformerException(Exception, HandwritingDataBase):
    """ Base class for TransformerException """

    def __init__(self, message):
        super(TransformerException, self).__init__(message)
        self.log(message)


class TransformerAngleTypeException(TransformerException):
    """ Exception raised for errors in the input angle type.

       Attributes:
           angle_type -- input angle_type which caused the error
           message -- explanation of the error
    """

    def __init__(self, angle_type):
        self.angle = angle_type

        if not self.angle:
            self.message = f"Angle type has not been specified! " \
                           f"Please select from ['{self.TILT}', '{self.AZIMUTH}']."
        else:
            self.message = f"Unknown Angle Type '{self.angle}' for HandwritingSample object instance. " \
                           f"Please select from ['{self.TILT}', '{self.AZIMUTH}']."
        
        super(TransformerAngleTypeException, self).__init__(self.message)