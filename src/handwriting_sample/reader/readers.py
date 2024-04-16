import os
import json

import numpy as np
import pandas as pd
from handwriting_sample.base import LoggableObject
from handwriting_sample.reader.exceptions import (HTMLPointerNotAllowedException,
                                                  HTMLDataMissingColumn,
                                                  HTMLDataMColumnMissingValues,
                                                  HTMLDataTransformationArgumentNotAllowed)
from handwriting_sample.transformer import HandwritingSampleTransformer


# ------------ #
# File readers #
# ------------ #

class JSONFileReader(LoggableObject):
    """Class implementing JSON file reader"""

    @classmethod
    def read(cls, path, verbose=False):
        """Reads the handwriting data and meta data"""

        # Read the handwriting data from a JSON file
        with open(path, "r") as file:
            json_data = json.load(file)

        # Get data and meta data
        data = json_data.get("data")
        meta = json_data.get("meta_data")
        cls.log(f"Data has been loaded from a JSON file: {path}", be_verbose=verbose)

        # Return data and meta data
        return data, meta


class SVCFileReader(LoggableObject):
    """Class implementing SVC file reader"""

    @classmethod
    def read(cls, path, column_names, verbose=False):
        """Reads the handwriting data and meta data"""

        # Read the handwriting data from an SVC file
        data = pd.read_csv(path, sep=" ", names=column_names, skiprows=1).to_dict(orient="list")
        meta = cls._read_metadata_from_svc_file_name(path)
        cls.log(f"Data has been loaded from an SVC file: {path}", be_verbose=verbose)

        # Return data and meta data
        return data, meta

    @classmethod
    def _read_metadata_from_svc_file_name(cls, file_path):
        """Reads meta data included in the file name"""

        # Prepare meta data
        meta_data = {}

        # Open file and read the first line
        with open(file_path) as f:
            raw_meta_data = f.readline()

        # Store the samples count
        meta_data["samples_count"] = int(raw_meta_data)

        # Get only file name and split it to get meta data from it
        file_path = os.path.basename(os.path.splitext(file_path)[0])
        meta_from_file_name = file_path.split("_")

        # Handle two optional information included in file name for HandAQUS
        if len(meta_from_file_name) >= 4:

            meta_data["participant"] = {"id": meta_from_file_name[0]}
            meta_data["created_on"] = meta_from_file_name[-1]
            meta_data["administrator"] = meta_from_file_name[-2]
            meta_data["task_id"] = meta_from_file_name[-3]

            if len(meta_from_file_name) == 6:
                meta_data["participant"] = {
                    "id": meta_from_file_name[0],
                    "birth_date": meta_from_file_name[1],
                    "sex": meta_from_file_name[2]
                }
        else:
            cls.log("Old file-name format no additional meta data")

        # Return meta data
        return meta_data


# ------------ #
# Data readers #
# ------------ #

class ListReader(LoggableObject):
    """Class implementing list object reader"""

    @classmethod
    def read(cls, data, column_names, verbose=False):
        """Reads the handwriting data and meta data"""

        # Get the handwriting data from a list object
        data = {column: value for column, value in zip(column_names, data)}
        meta = {}
        cls.log(f"Data has been loaded from a list", be_verbose=verbose)

        # Return data and meta data
        return data, meta


class NumpyArrayReader(LoggableObject):
    """Class implementing numpy array reader"""

    @classmethod
    def read(cls, data, column_names, verbose=False):
        """Reads the handwriting data and meta data"""

        # Get the handwriting data from a list object
        data = {column: data[..., i] for i, column in enumerate(column_names)}
        meta = {}
        cls.log(f"Data has been loaded from a numpy array", be_verbose=verbose)

        # Return data and meta data
        return data, meta


class PandasDataFrameReader(LoggableObject):
    """Class implementing pandas dataframe reader"""

    @classmethod
    def read(cls, data, verbose=False):
        """Reads the handwriting data and meta data"""

        # Get the handwriting data from a list object
        data = data.to_dict(orient="list")
        meta = {}
        cls.log(f"Data has been loaded from a pandas dataframe", be_verbose=verbose)

        # Return data and meta data
        return data, meta


class HTMLPointerEventReader(LoggableObject):
    """Class implementing HTML Pointer Event reader"""

    # Handwriting data
    HTML_AXIS_X = "x"
    HTML_AXIS_Y = "y"
    HTML_TIME = "time"
    HTML_BUTTONS = "buttons"
    HTML_BUTTON = "button"
    HTML_TILT_X = "tiltX"
    HTML_TILT_Y = "tiltY"
    HTML_PRESSURE = "pressure"
    HTML_TWIST = "twist"
    POINTER_TYPE = "pointerType"

    HTML_DEFAULT_TIME_CONVERSION = 1000

    # Columns
    ALL_HTML_COLUMNS = [HTML_AXIS_X, HTML_AXIS_Y, HTML_TIME, HTML_BUTTON, HTML_BUTTONS, HTML_TILT_X, HTML_TILT_Y,
                        HTML_PRESSURE, HTML_TWIST, POINTER_TYPE]
    USEFUL_HTML_COLUMNS = [HTML_AXIS_X, HTML_AXIS_Y, HTML_TIME, HTML_BUTTONS, HTML_PRESSURE, HTML_TILT_X, HTML_TILT_Y]

    # Allowed pointer types
    ALLOWED_POINTER_TYPES = ["pen"]

    @classmethod
    def read(cls, data, verbose=False, **kwargs):
        """
        Reads the handwriting data and meta data

        :param data: data representing handwriting sample by HTML Pointer Event
        :type data: dict
        :param verbose: verbosity of the logging, defaults to False
        :type verbose: bool, optional

        :return: data and meta data
        :rtype: tuple
        """

        # Check if the pointer type is allowed
        if data.get(cls.POINTER_TYPE) not in cls.ALLOWED_POINTER_TYPES:
            raise HTMLPointerNotAllowedException(f"Pointer type {data.get(cls.POINTER_TYPE)} is not allowed for "
                                                 f"Handwriting Sample.")

        # Get the handwriting data from a list object
        data = cls._transform_html_data_to_sample_data(data, **kwargs)
        meta = {}
        cls.log(f"Data has been loaded from a HTML pointer event data", be_verbose=verbose)

        # Return data and meta data
        return data, meta

    @classmethod
    def _transform_html_data_to_sample_data(cls,
                                            html_data,
                                            transform_x_y_to_mm=True,
                                            transform_time_to_seconds=True,
                                            transform_tilt_xy_to_azimuth_and_tilt=True,
                                            revert_y_axis=True,
                                            transform_pressure=True,
                                            **kwargs):
        """Transforms HTML data to sample data"""

        allowed_kwargs = ["time_conversion",
                          "tablet_pixel_resolution",
                          "tablet_mm_dimensions",]

        # Check if all data from useful columns are present
        if not all([column in html_data.keys() for column in cls.USEFUL_HTML_COLUMNS]):
            raise HTMLDataMissingColumn(f"Pointer event data does not contain all required columns. "
                                        f"Required columns: {cls.USEFUL_HTML_COLUMNS}")

        # Transform data check if any column is empty
        for column in cls.USEFUL_HTML_COLUMNS:
            if not html_data.get(column):
                raise HTMLDataMColumnMissingValues(f"Pointer event data contains empty column: {column}.")

        # Check kwargs
        if kwargs:
            for key in kwargs.keys():
                if key not in allowed_kwargs:
                    raise HTMLDataTransformationArgumentNotAllowed(f"Unknown keyword argument: {key}")

        # Get kwargs
        time_conversion = kwargs.get("time_conversion", cls.HTML_DEFAULT_TIME_CONVERSION)
        tablet_pixel_resolution = kwargs.get("tablet_pixel_resolution", None)
        tablet_mm_dimensions = kwargs.get("tablet_mm_dimensions", None)

        # Transform tilt_X and tilt_Y azimuth and tilt
        if transform_tilt_xy_to_azimuth_and_tilt:
            azimuth, tilt = HandwritingSampleTransformer.transform_tilt_xy_to_azimuth_and_tilt(html_data.get(cls.HTML_TILT_X),
                                                                                               html_data.get(cls.HTML_TILT_Y))
        else:
            azimuth = html_data.get(cls.HTML_TILT_X)
            tilt = html_data.get(cls.HTML_TILT_Y)

        # Transform time from microseconds to seconds and shift to 0
        if transform_time_to_seconds:
            times = [(time - html_data.get(cls.HTML_TIME)[0]) / time_conversion for time in html_data.get(cls.HTML_TIME)]
            html_data[cls.HTML_TIME] = times

        # Transform x,y to mm
        if transform_x_y_to_mm:

            # Check if we have kwargs
            if tablet_pixel_resolution or tablet_mm_dimensions:
                # Check if tuple
                if not isinstance(tablet_pixel_resolution, tuple) or not isinstance(tablet_mm_dimensions, tuple):
                    raise HTMLDataTransformationArgumentNotAllowed(f"Both tablet_pixel_resolution "
                                                                   f"and tablet_mm_dimensions must be tuple.")

                px_to_mm = tablet_mm_dimensions[0] / tablet_pixel_resolution[0]

            else:
                # Default PX to MM
                px_to_mm = HandwritingSampleTransformer.PX_TO_MM

            html_data[cls.HTML_AXIS_X] = [x * px_to_mm for x in html_data.get(cls.HTML_AXIS_X)]
            html_data[cls.HTML_AXIS_Y] = [y * px_to_mm for y in html_data.get(cls.HTML_AXIS_Y)]

        # Revert Y axis
        if revert_y_axis:
            # Get max Y value form kwarg, if not set use default
            max_y_value_mm = kwargs.get("max_y_value_mm", None)
            if not max_y_value_mm:
                max_y_value_mm = HandwritingSampleTransformer.DEFAULT_MM_DIMENSIONS[1]

            ax_data = np.array(html_data[cls.HTML_AXIS_Y])
            html_data[cls.HTML_AXIS_Y] = HandwritingSampleTransformer.revert_axis(ax_data, max_y_value_mm)

        # Transform pressure
        if transform_pressure:
            pressure_levels = kwargs.get("pressure_levels", None)
            if not pressure_levels:
                pressure_levels = HandwritingSampleTransformer.PRESSURE_LEVELS

            # Multiply each value of pressure by the number of pressure levels
            html_data[cls.HTML_PRESSURE] = [pressure * pressure_levels for pressure in html_data.get(cls.HTML_PRESSURE)]


        # Transform data for Handwriting Sample
        sample_data = {
            "x": html_data.get(cls.HTML_AXIS_X),
            "y": html_data.get(cls.HTML_AXIS_Y),
            "time": html_data.get(cls.HTML_TIME),
            "pen_status": html_data.get(cls.HTML_BUTTONS),
            "azimuth": azimuth,
            "tilt": tilt,
            "pressure": html_data.get(cls.HTML_PRESSURE)
        }

        return sample_data


