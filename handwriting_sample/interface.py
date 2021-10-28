import numpy as np
import pandas as pd
from datetime import datetime
from handwriting_sample.base import HandwritingDataBase
from handwriting_sample.reader import HandwritingSampleReader
from handwriting_sample.writer import HandwritingSampleWriter
from handwriting_sample.validator import HandwritingSampleValidator


class HandwritingSample(HandwritingDataBase):
    """Class implementing the management of sample handwriting samples"""

    # Handwriting data helpers (reading, writing, validation)
    reader = HandwritingSampleReader()
    writer = HandwritingSampleWriter()
    validator = HandwritingSampleValidator()

    # TODO: idea: I think np.column_stack is going to work if X, Y, etc. are 1D numpy arrays as well
    def __init__(self, x, y, time, pen_status, azimuth, tilt, pressure, meta_data=None, validate=True):
        """
        Initializes the HandwritingSample object.

        :param x: X axis
        :type x: list[uint]
        :param y: Y axis
        :type y: list[uint]
        :param time: timestamp
        :type time: list[uint]
        :param pen_status: indication of pen location (on-surface=1 | in-air=0)
        :type pen_status: list[bool]
        :param azimuth: azimuth of the pen
        :type azimuth: list[uint]
        :param tilt: tilt of the pen
        :type tilt: list[uint]
        :param pressure: pressure value
        :type pressure: list[uint]
        :param meta_data: dictionary with meta data
        :type meta_data: dict
        :param validate: true is validate input data
        :type validate:bool
        """

        # Create pandas DataFrame object from the input handwriting variables
        df = pd.DataFrame(np.column_stack([x, y, time, pen_status, azimuth, tilt, pressure]), columns=self.COLUMNS)

        # Validate and store input data
        self._data = self.validator.validate_data(df) if validate else df

        # Store meta data of any kind
        self.meta = meta_data

        # Set the handwriting variables
        self.x = self._data[self.AXIS_X].to_numpy()
        self.y = self._data[self.AXIS_Y].to_numpy()
        self.time = self._data[self.TIME].to_numpy()
        self.pen_status = self._data[self.PEN_STATUS].to_numpy(dtype=bool)
        self.azimuth = self._data[self.AZIMUTH].to_numpy()
        self.tilt = self._data[self.TILT].to_numpy()
        self.pressure = self._data[self.PRESSURE].to_numpy()

    def __repr__(self):
        return f"<HandwritingSampleObject: \n" \
               f"DATA:\n" \
               f"   x =          {self.x}, \n" \
               f"   y =          {self.y}, \n" \
               f"   time =       {self.time}, \n" \
               f"   pen_status = {self.pen_status}, \n" \
               f"   azimuth =    {self.azimuth}, \n" \
               f"   tilt =       {self.tilt}, \n" \
               f"   pressure =   {self.pressure}> \n\n\n" \
               f"METADATA:\n" \
               f"{self.meta.items() if self.meta else None}"

    # ---------- #
    # Properties #
    # ---------- #

    @property
    def data_list(self):
        """Returns list for the non-original data"""
        return [self.x, self.y, self.time, self.pen_status, self.azimuth, self.tilt, self.pressure]

    @property
    def data_numpy_array(self):
        """Returns numpy array for the non-original data"""
        return np.column_stack(self.data_list)

    @property
    def data_pandas_dataframe(self):
        """Returns pandas DataFrame for the non-original data"""
        return pd.DataFrame(self.data_numpy_array, columns=self.COLUMNS)

    @property
    def original_data_list(self):
        """Returns list for the original data"""
        return [self._data[column].to_numpy() for column in self._data.columns]

    @property
    def original_numpy_array(self):
        """Returns numpy array for the original data"""
        return self._data.values

    @property
    def original_data_pandas_dataframe(self):
        """Returns pandas DataFrame for the original data"""
        return self._data

    @property
    def xy(self):
        """Returns general movement of X and Y"""
        return np.sqrt(np.power(self.x, 2) + np.power(self.y, 2))

    # --------------- #
    # Reading methods #
    # --------------- #

    @classmethod
    def from_json(cls, path, columns=None):
        """
        Creates a HandwritingSample instance from a JSON file.

        :param path: path to a JSON file
        :type path: str
        :param columns: handwriting variables, defaults to cls.COLUMNS
        :type columns: list, optional
        :return: instance of HandwritingSample
        :rtype: HandwritingSample
        """
        return cls._from_data_and_metadata(*cls.reader.read_from_json(path, columns or cls.COLUMNS))

    @classmethod
    def from_svc(cls, path, columns=None):
        """
        Creates a HandwritingSample instance from an SVC file.

        :param path: path to an SVC file
        :type path: str
        :param columns: handwriting variables, defaults to cls.COLUMNS
        :type columns: list, optional
        :return: instance of HandwritingSample
        :rtype: HandwritingSample
        """
        return cls._from_data_and_metadata(*cls.reader.read_from_svc(path, columns or cls.COLUMNS))

    @classmethod
    def from_list(cls, data, columns=None):
        """
        Creates a HandwritingSample instance from a list.

        :param data: data representing handwriting sample
        :type data: list
        :param columns: handwriting variables, defaults to cls.COLUMNS
        :type columns: list, optional
        :return: instance of HandwritingSample
        :rtype: HandwritingSample
        """
        return cls._from_data_and_metadata(*cls.reader.read_from_list(data, columns or cls.COLUMNS))

    @classmethod
    def from_numpy_array(cls, data, columns=None):
        """
        Creates a HandwritingSample instance from a numpy array.

        :param data: data representing handwriting sample
        :type data: np.ndarray
        :param columns: handwriting variables, defaults to cls.COLUMNS
        :type columns: list, optional
        :return: instance of HandwritingSample
        :rtype: HandwritingSample
        """
        return cls._from_data_and_metadata(*cls.reader.read_from_numpy_array(data, columns or cls.COLUMNS))

    @classmethod
    def from_pandas_dataframe(cls, data, columns=None):
        """
        Creates a HandwritingSample instance from a pandas DataFrame.

        :param data: data representing handwriting sample
        :type data: pd.DataFrame
        :param columns: handwriting variables, defaults to cls.COLUMNS
        :type columns: list, optional
        :return: instance of HandwritingSample
        :rtype: HandwritingSample
        """
        return cls._from_data_and_metadata(*cls.reader.read_from_pandas_dataframe(data, columns or cls.COLUMNS))

    @classmethod
    def _from_data_and_metadata(cls, data, meta_data=None):
        """
        Creates a HandwritingSample instance from data and meta data.

        :param data: data of the handwriting sample
        :type data: dict
        :param meta_data: meta data of the handwriting sample, defaults to None
        :type meta_data: dict, optional
        :return: instance of HandwritingSample
        :rtype: HandwritingSample
        """
        return cls(**data, meta_data=meta_data or {})

    # --------------- #
    # Writing methods #
    # --------------- #

    def to_json(self, path, file_name=None, store_original_data=False):
        """
        Writes sample data to a JSON file.

        :param path: path where data should be stored
        :type path: str
        :param file_name: custom file name, defaults to None
        :type file_name: str, optional
        :param store_original_data: store original data, defaults to False
        :type store_original_data: bool, optional
        :return: None
        :rtype: None type
        """
        return self.writer.write_to_json(self, path, file_name=file_name, store_original_data=store_original_data)

    def to_svc(self, path, file_name=None, store_original_data=False):
        """
        Writes sample data to an SVC file.

        :param path: path where data should be stored
        :type path: str
        :param file_name: custom file name, defaults to None
        :type file_name: str, optional
        :param store_original_data: store original data, defaults to False
        :type store_original_data: bool, optional
        :return: None
        :rtype: None type
        """
        return self.writer.write_to_svc(self, path, file_name=file_name, store_original_data=store_original_data)

    # ----------------------------- #
    # Handwriting data manipulation #
    # ----------------------------- #

    def get_on_surface_data(self):
        """Returns on-surface data as a HandwritingSample object"""

        # Get all on-surface data
        df = self.data_pandas_dataframe
        df = df[df[self.PEN_STATUS] == 1]

        # Return a new instance of HandwritingSample with only on-surface data
        return HandwritingSample(**df.to_dict(orient="list"), validate=False)

    def get_in_air_data(self):
        """Returns in-air data as a HandwritingSample object"""

        # Return all in-air data
        df = self.data_pandas_dataframe
        df = df[df[self.PEN_STATUS] == 0]

        # Return a new instance of HandwritingSample with only in-air data
        return HandwritingSample(**df.to_dict(orient="list"), validate=False)

    def get_on_surface_strokes(self):
        """Returns strokes on-surface"""
        return self.get_strokes(on_surface_only=True)

    def get_in_air_strokes(self):
        """Returns strokes in-air"""
        return self.get_strokes(in_air_only=True)

    def get_strokes(self, on_surface_only=False, in_air_only=False):
        """
        Splits the movement into strokes.

        :param on_surface_only: on-surface strokes only, defaults to False
        :type on_surface_only: bool, optional
        :param in_air_only: in-air strokes only, defaults to True
        :type in_air_only: bool, optional
        :return: list of strokes in tuples with the status of strokes
        :rtype: tuple('status', HandwritingSample)
        """

        # Handle the edge cases
        if all((on_surface_only, in_air_only)):
            on_surface_only, in_air_only = False, False

        # Get accessible data of the sample as a pandas DataFrame
        df = self.data_pandas_dataframe

        # Get index values of the pen status column changes
        idx_change = df.ne(df.shift()).filter(like=self.PEN_STATUS).apply(lambda x: x.index[x].tolist())
        idx_array = idx_change[self.PEN_STATUS].values.tolist()

        # Add the last index value
        idx_array.append(df.index[-1])

        # Get strokes
        strokes = [df.iloc[idx_array[n]:idx_array[n + 1]] for n in range(len(idx_array) - 1)]

        # Prepare the list of strokes
        list_of_strokes = []

        # Fill the list of strokes (add 'on_surface'/'in_air' flag in front of each stroke)
        for stroke in strokes:

            # If on surface strokes only are wanted filter out in air
            if on_surface_only and stroke[self.PEN_STATUS].iloc[0] == 0:
                continue

            # If in air strokes only are wanted filter out on surface
            if in_air_only and stroke[self.PEN_STATUS].iloc[0] == 1:
                continue

            # Prepare the stroke information
            status = "on_surface" if stroke[self.PEN_STATUS].iloc[0] == 1 else "in_air"
            stroke = HandwritingSample(**stroke.to_dict(orient="list"), validate=False)

            # Append to the list of strokes
            list_of_strokes.append((status, stroke))

        # Return the list of strokes
        return list_of_strokes

    # ---------------------- #
    # Meta data manipulation #
    # ---------------------- #

    def add_meta_data(self, meta_data):
        """Adds meta data to the HandwritingSample object from dictionary"""
        self.meta.update({"updated_on": datetime.utcnow().strftime(self.DATE_FORMAT)})
        self.meta.update({**meta_data})
