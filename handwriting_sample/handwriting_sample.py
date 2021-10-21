import numpy as np
import pandas as pd
from datetime import datetime
from handwriting_sample.base import HandwritingDataBase
from handwriting_sample.sample_read import SampleRead
from handwriting_sample.sample_store import SampleStore


class HandwritingSample(HandwritingDataBase):
    """Class implementing the management of sample handwriting samples"""

    # Handwriting data reader and writer
    reader = SampleRead()
    writer = SampleStore()

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
        :type pen_status: lis[bool]
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

        # Create pandas DataFrame object from input values
        df = pd.DataFrame(np.column_stack([x, y, time, pen_status, azimuth, tilt, pressure]), columns=self.COLUMNS)

        # Validate and store input data
        self._data = self.reader.validate_data(df) if validate else df

        # Store metadata of any kind
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
    def data_dataframe(self):
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
    def original_data_dataframe(self):
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
    def from_json(cls, path):
        """Creates a HandwritingSample instance from a JSON file"""

        # Read data from a JSON file
        data, meta_data = cls.reader.read_from_json(path)

        # Return data and meta_data
        return cls(**data, meta_data=meta_data)

    @classmethod
    def from_svc(cls, path, column_names=None):
        """Creates a HandwritingSample instance from an SVC file"""

        # Read data from an SVC file
        data, meta_data = cls.reader.read_from_svc(path, column_names=column_names)

        # Return data and meta_data
        return cls(**data, meta_data=meta_data)

    @classmethod
    def from_list(cls, array, column_names=None):
        """Creates the HandwritingSample instance from a list"""
        return cls(**cls.reader.read_from_list(array, column_names=column_names))

    @classmethod
    def from_pandas_dataframe(cls, df):
        """Creates a HandwritingSample instance from a pandas DataFrame"""
        return cls(**cls.reader.read_from_pandas_dataframe(df))

    # --------------- #
    # Writing methods #
    # --------------- #

    def to_json(self, path, data=None, original_data=False, file_name=None):
        """
        Stores sample data to a JSON file.

        :param path: path where data should be stored
        :type path: str
        :param data: custom data to be stored, defaults to accessible data
        :type data: pd.DataFrame, optional
        :param original_data: store original data, defaults to False
        :type original_data: bool, optional
        :param file_name: custom file name, defaults to None
        :type file_name: str, optional
        """
        self.writer.store_to_json(
            data=self.original_data_dataframe if original_data else (data if data else self.data_dataframe),
            save_path=path,
            file_name=file_name)

    def to_svc(self, path, data=None, original_data=False, file_name=None):
        """
        Stores sample data to an SVC file.

        :param path: path where data should be stored
        :type path: str
        :param data: custom data to be stored, defaults to accessible data
        :type data: pd.DataFrame, optional
        :param original_data: store original data, defaults to False
        :type original_data: bool, optional
        :param file_name: custom file name, defaults to None
        :type file_name: str, optional
        """
        self.writer.store_to_svc(
            data=self.original_data_dataframe if original_data else (data if data else self.data_dataframe),
            save_path=path,
            file_name=file_name)

    # ----------------------------- #
    # Handwriting data manipulation #
    # ----------------------------- #

    def get_on_surface_data(self):
        """Returns on-surface data as a HandwritingSample object"""

        # Get accessible data of the sample as a pandas DataFrame
        df = self.data_dataframe

        # Get all on-surface data
        data = df[df[self.PEN_STATUS] == 0]

        # Return a new instance of HandwritingSample with only on-surface data
        return HandwritingSample(**data.to_dict(orient="list"), validate=False)

    def get_in_air_data(self):
        """Returns in-air data as a HandwritingSample object"""

        # Get accessible data of the sample as a pandas DataFrame
        df = self.data_dataframe

        # Return all in-air data
        data = df[df[self.PEN_STATUS] == 0]

        # Return a new instance of HandwritingSample with only in-air data
        return HandwritingSample(**data.to_dict(orient="list"), validate=False)

    def get_on_surface_strokes(self):
        """Returns strokes on-surface"""
        return self.get_strokes(on_surface_only=True)

    def get_in_air_strokes(self):
        """Returns strokes in-air"""
        return self.get_strokes(in_air_only=True)

    def get_strokes(self, on_surface_only=False, in_air_only=False):
        """Splits the movement into strokes.

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
        df = self.data_dataframe

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
