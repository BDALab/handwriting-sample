import os
import json
import pandas as pd
from handwriting_sample.base import HandwritingDataBase


class SampleRead(HandwritingDataBase):
    """Class implementing reading and validating of handwriting data"""

    # --------------- #
    # Reading methods #
    # --------------- #

    @classmethod
    def read_from_json(cls, path, verbose=False):
        """Reads data from a JSON file"""

        # Read the JSON file
        with open(path, "r") as file:
            json_data = json.load(file)

        # Get data and meta data
        data = json_data.get("data")
        meta = json_data.get("meta_data")
        cls.log(f"Data has been loaded from: {path}", be_verbose=verbose)

        # Return data and meta_data
        return data, meta

    @classmethod
    def read_from_svc(cls, path, column_names=None, verbose=False):
        """Reads data from an SVC file"""

        # Prepare the column names
        column_names = column_names if column_names else cls.COLUMNS

        # Get data (skip first row with meta data) and meta data
        data = pd.read_csv(path, sep=" ", names=column_names, skiprows=1).to_dict(orient="list")
        meta = cls._read_metadata_from_svc_file_name(path)
        cls.log(f"Data has been loaded from: {path}", be_verbose=verbose)

        # Return data and meta_data
        return data, meta

    @classmethod
    def read_from_list(cls, array, column_names=None):
        """Reads data from a list"""
        return {key: value for key, value in zip(column_names if column_names else cls.COLUMNS, array)}

    @classmethod
    def read_from_pandas_dataframe(cls, df_data):
        """Creates data from a pandas DataFrame"""
        return df_data.to_dict(orient="list")

    # ------------------ #
    # Validation methods #
    # ------------------ #

    @classmethod
    def validate_data(cls, df_data):
        """Validates input data (already in pandas DataFrame)"""

        # Set column names to lower case
        df_data.columns = [x.lower() for x in df_data.columns]

        # Get column count
        columns = df_data.columns

        # Check for number of time-series
        if len(columns) < len(cls.COLUMNS):
            raise ValueError(
                f"Input data are missing the following mandatory time-series (columns): "
                f"{list(set(columns).symmetric_difference(set(cls.COLUMNS)))}")
        if len(columns) > len(cls.COLUMNS):
            raise ValueError(
                f"Input data have unwanted time-series that are not expected in the data: "
                f"{list(set(columns).symmetric_difference(set(cls.COLUMNS)))}")

        # Check for missing values:
        if df_data.isnull().sum().sum() > 0:
            raise ValueError(
                f"Empty values in input data. Please inspect your input and replace the emtpy values. \n"
                f"The following table shows the count of emtpy values in particular columns: \n"
                f"{df_data.isnull().sum()}")

        # Check if the values are numerical
        for column_name in columns:
            if not all(isinstance(x, (int, float)) for x in df_data[column_name]):
                raise ValueError(f"Datatype in time-series [\'{column_name}\'] is not numerical")

        # Order the columns based on the pre-defined order
        df_data = df_data[cls.COLUMNS]

        # Remove any in-air movement on the boundaries
        cls._remove_first_in_air_data(df_data)
        cls._remove_last_in_air_data(df_data)

        # TODO: validate data range
        return df_data

    # --------------- #
    # Utility methods #
    # --------------- #

    @classmethod
    def _remove_first_in_air_data(cls, df):
        """Removes unwanted in-air movement at the beginning of writing"""
        cls.log(f"Check if data contains first in-air movement (unwanted before writing)")

        # Check if the first sample has any in air movement
        if df[cls.PEN_STATUS].iloc[0] == 1:
            cls.log(f"Data do not contain any in-air movement at the beginning")
            return

        # Remove in-air data at the beginning
        cls.log(f"Data contains in-air movement at the beginning")

        count = 0
        for index, row in df.iterrows():
            if row[cls.PEN_STATUS] == 0:
                df.drop(index, inplace=True)
                count += 1
            else:
                cls.log(f"Removed first {count} in-air samples")
                df.reset_index(inplace=True)
                return

    @classmethod
    def _remove_last_in_air_data(cls, df):
        """Removes unwanted in-air movement at the end of writing"""
        cls.log(f"Check if data contains last in-air movement (unwanted after writing)")

        # Check if last sample has any in-air movement
        if df[cls.PEN_STATUS].iloc[-1] == 1:
            cls.log(f"Data do not contain any in-air movement at the end")
            return

        # Remove in-air data at the end
        cls.log(f"Data contains in-air movement at the beginning")

        count = 0
        for index in range(df.shape[0] - 1, -1, -1):
            if df[cls.PEN_STATUS].iloc[index] == 0:
                df.drop(index, inplace=True)
                count += 1
            else:
                cls.log(f"Removed last {count} in-air samples")
                df.reset_index(inplace=True)
                return

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
