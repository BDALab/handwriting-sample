import os
import json
import pandas as pd
from src.handwriting_sample.base import LoggableObject


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
