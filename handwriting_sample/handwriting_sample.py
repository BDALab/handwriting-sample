from datetime import datetime

import numpy as np
import pandas as pd

from handwriting_sample.base import Base
from handwriting_sample.sample_read import SampleRead
from handwriting_sample.sample_store import SampleStore

from functools import cached_property


class HandwritingSample(Base):
    """ Class implementing the management of sample """

    # Define reader
    reader = SampleRead(Base.COLUMN_NAMES)

    def __init__(self,
                 x,
                 y,
                 time,
                 pen_status,
                 azimuth,
                 tilt,
                 pressure,
                 meta_data=None,
                 validate=True):
        """
        Initialize the HandwritingSample object.

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
        :param validate: true is validate intpu data
        :type validate:bool
        """

        if not self.COLUMN_NAMES:
            raise ValueError(f"Column names must be specified! COLUMN_NAMES = {self.COLUMN_NAMES}")

        # Create dataframe from input values
        df_data = pd.DataFrame(np.column_stack([x, y, time, pen_status, azimuth, tilt, pressure]),
                               columns=self.COLUMN_NAMES)

        # Validate input data and store to protected
        if validate:
            self._data = self.reader.validate_data(df_data)
        else:
            self._data = df_data

        # Store metadata of any kind
        self.meta_data = meta_data

        # Store date to accessible separate arrays
        self.x = self._data[self.AX_X].to_numpy()
        self.y = self._data[self.AX_Y].to_numpy()
        self.time = self._data[self.TIME].to_numpy()
        self.pen_status = self._data[self.PEN_STATUS].to_numpy(dtype=bool)
        self.azimuth = self._data[self.AZIMUTH].to_numpy()
        self.tilt = self._data[self.TILT].to_numpy()
        self.pressure = self._data[self.PRESSURE].to_numpy()

        # Prepare store
        self.store = SampleStore()

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
               f"{self.meta_data.items() if self.meta_data else None}"

    @cached_property
    def xy(self):
        """ Return general movement of X and Y """
        return np.sqrt(np.power(self.x, 2) + np.power(self.y, 2))

    @classmethod
    def from_json(cls, path_to_json):
        """
        Creates the HandwritingSample instance utilizing the reader.

        :param path_to_json: path to the json file
        :type path_to_json: str

        :return: HandwritingSample class instance
        """

        # Read data from json
        data, metadata = cls.reader.read_from_json(path_to_json)

        # Return data and meta_data
        return cls(**data, meta_data=metadata)

    @classmethod
    def from_svc(cls, path_to_svc, column_names=None):
        """
        Creates the HandwritingSample instance utilizing the reader.

        :param path_to_svc: path to the svc file
        :type path_to_svc: str
        :param column_names: column names in order as in input data
        :type column_names: list['str']

        :return: HandwritingSample class instance
        """

        # Read data from svc
        data, meta_data = cls.reader.read_from_svc(path_to_svc, column_names=column_names)

        # Return data and meta_data
        return cls(**data, meta_data=meta_data)

    @classmethod
    def from_pandas(cls, df_data):
        """
        Creates the HandwritingSample instance from pandas

        :param df_data: data in pandas dataframe
        :type df_data: pd.DataFrame

        :return: HandwritingSample class instance
        """

        # Return data
        return cls(**df_data.to_dict(orient='list'))

    @classmethod
    def from_array(cls, array_data, column_names=None):
        """
        Creates the HandwritingSample instance from array.

        :param array_data: data in pandas dataframe
        :type array_data: pd.DataFrame
        :param column_names: column names in order as in input data
        :type column_names: list['str']

        :return: HandwritingSample class instance
        """

        # Return data
        return cls(**cls.reader.read_from_array(array_data, column_names=column_names))

    def to_json(self,
                path_to_store,
                data=None,
                original_data=False,
                file_name=None):
        """
        Store sample data to JSON. Stores accessible data by DEFAULT.

        :param path_to_store: path where data should be stored
        :type path_to_store: str
        :param data: Custom data to be stored (must follow the columns of HandwritingSample class)
        :type data: pd.DataFrame
        :param original_data: Set to true if original loaded data should be stored
        :type original_data: bool
        :param file_name: custom file name
        :type file_name: str
        """

        # Store data
        self.store_data(path_to_store,
                        data=data,
                        original_data=original_data,
                        file_name=file_name,
                        to_json=True)

    def to_svc(self,
               path_to_store,
               data=None,
               original_data=False,
               file_name=None):
        """
        Store sample data to SVC. Stores accessible data by DEFAULT.

        :param path_to_store: path where data should be stored
        :type path_to_store: str
        :param data: Custom data to be stored (must follow the columns of HandwritingSample class)
        :type data: pd.DataFrame
        :param original_data: Set to true if original loaded data should be stored
        :type original_data: bool
        :param file_name: custom file name
        :type file_name: str
        """

        # Store data
        self.store_data(path_to_store,
                        data=data,
                        original_data=original_data,
                        file_name=file_name,
                        to_svc=True)

    def store_data(self,
                   path_to_store,
                   data=None,
                   original_data=False,
                   to_json=False,
                   to_svc=False,
                   file_name=None):
        """ Wrapper function for data storage"""

        # Prepare data to store
        if original_data:
            # Store original loaded data
            data = self._data

        elif not data:
            # Store accessible data
            data = self.get_df_sample_accessible_data()

        # Store Data
        self.store.store_data(data,
                              path_to_store,
                              to_json=to_json,
                              to_svc=to_svc,
                              meta_data=self.meta_data,
                              file_name=file_name)

    def get_df_sample_accessible_data(self):
        """ Get handwriting sample accessible data in pandas dataframe"""

        return pd.DataFrame(np.column_stack([self.x,
                                             self.y,
                                             self.time,
                                             self.pen_status,
                                             self.azimuth,
                                             self.tilt,
                                             self.pressure]),
                            columns=self.COLUMN_NAMES)

    def add_meta_data(self, meta_data):
        """
        Add meta data to the HandwritingSample object from dictionary

        :param meta_data: meta data
        :type meta_data: dict
        """

        # Add metadata
        self.meta_data.update({'updated_on': datetime.utcnow().strftime(self.DATE_FORMAT)})
        self.meta_data.update({**meta_data})

    def get_on_surface_data(self):
        """ Returns the on surface data """

        # Get accessible data (not original) of the sample in pd.DataFrame
        df_accessible_data = self.get_df_sample_accessible_data()

        # Return all on surface data
        on_surface_data = df_accessible_data[df_accessible_data[self.PEN_STATUS] == 1]

        # Return all in air data
        return HandwritingSample(**on_surface_data.to_dict(orient='list'), validate=False)

    def get_in_air_data(self):
        """ Returns the in air data """

        # Get accessible data (not original) of the sample in pd.DataFrame
        df_accessible_data = self.get_df_sample_accessible_data()

        in_air_data = df_accessible_data[df_accessible_data[self.PEN_STATUS] == 0]

        # Return all in air data
        return HandwritingSample(**in_air_data.to_dict(orient='list'), validate=False)

    def get_on_surface_strokes(self):
        """ Get strokes on surface"""
        return self.get_strokes(on_surface_only=True)

    def get_in_air_strokes(self):
        """ Get strokes in air"""
        return self.get_strokes(in_air_only=True)

    def get_strokes(self,
                    on_surface_only=False,
                    in_air_only=False):
        """
        Split the movement in separate strokes

        :param on_surface_only: Set to true to get only on surface strokes
        :type on_surface_only: bool
        :param in_air_only: Set to true to get only in air strokes
        :type in_air_only: true

        :return: list of strokes in tuples with the status of stroke
        :rtype: tuple('status', HandwritingSample)
        """

        # Get accessible data (not original) of the sample in pd.DataFrame
        df_accessible_data = self.get_df_sample_accessible_data()

        # Get index values of Pen_status column changes
        idx_change = df_accessible_data.ne(df_accessible_data.shift()).filter(like=self.PEN_STATUS).apply(lambda x: x.index[x].tolist())
        idx_list = idx_change[self.PEN_STATUS].values.tolist()

        # Add last index value
        idx_list.append(df_accessible_data.index[-1])

        # Get Strokes
        strokes = [df_accessible_data.iloc[idx_list[n]:idx_list[n + 1]] for n in range(len(idx_list) - 1)]

        # Add 'on_surface'/'in_air' flag in front of stroke (tuple)
        list_strokes = []
        for stroke in strokes:

            # If on surface strokes only are wanted filter out in air
            if on_surface_only and stroke[self.PEN_STATUS].iloc[0] == 0:
                continue

            # If in air strokes only are wanted filter out on surface
            if in_air_only and stroke[self.PEN_STATUS].iloc[0] == 1:
                continue

            # get status and append to list
            status = 'on_surface' if stroke[self.PEN_STATUS].iloc[0] == 1 else 'in_air'
            list_strokes.append((status, HandwritingSample(**stroke.to_dict(orient='list'), validate=False)))

        return list_strokes