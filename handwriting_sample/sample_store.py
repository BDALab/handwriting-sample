import json
import pandas as pd
from datetime import datetime
from handwriting_sample.base import HandwritingDataBase
from handwriting_sample.sample_read import SampleRead


class SampleStore(HandwritingDataBase):
    """Class implementing writing and validating of handwriting data"""

    # --------------- #
    # Writing methods #
    # --------------- #

    def store_to_json(self, data, save_path, meta_data=None, file_name=None):
        """
        Stores HandwritingSample data to a JSON file.

        :param data: input data
        :type data: pd.DataFrame
        :param save_path: save path
        :type save_path: str
        :param meta_data: meta data, defaults to None
        :type meta_data: dict, optional
        :param file_name: file name (optional if meta data), defaults to None
        :type file_name: str, optional
        :return: True if stored, False otherwise
        :rtype: bool
        """

        # Validate the output data
        data = self.validate_data(data).to_dict("list")

        # Prepare meta data
        meta_data = self._prepare_meta_data(meta_data)

        # If the filename is not set, create a default one
        if not file_name and meta_data:
            file_name = self._collect_file_name(meta_data)

        # Update the save_path
        save_path = f"{save_path}/{file_name}.json"

        # Store the data
        try:
            with open(save_path, "w") as f:
                json.dump({"meta_data": meta_data, "data": data}, f)
                self.log(f"Data stored in {save_path}")
                return True

        except Exception:
            self.log(f"Unable to store the file {save_path}")
            raise

    def store_to_svc(self, data, save_path, meta_data=None, file_name=None):
        """
        Stores HandwritingSample data to an SVC file.

        :param data: input data
        :type data: pd.DataFrame
        :param save_path: save path
        :type save_path: str
        :param meta_data: meta data, defaults to None
        :type meta_data: dict, optional
        :param file_name: file name (optional if meta data), defaults to None
        :type file_name: str, optional
        :return: True if stored, False otherwise
        :rtype: bool
        """

        # Validate the output data
        data = self.validate_data(data).to_dict("r")

        # Prepare meta data
        meta_data = self._prepare_meta_data(meta_data)

        # If the filename is not set, create a default one
        if not file_name and meta_data:
            file_name = self._collect_file_name(meta_data)

        # Update the save_path
        save_path = f"{save_path}/{file_name}.svc"

        # Prepare the data to be stored
        data = [
            f"{row[self.AXIS_X]} {row[self.AXIS_Y]} "
            f"{row[self.TIME]} {row[self.PEN_STATUS]} "
            f"{row[self.AZIMUTH]} {row[self.TILT]} "
            f"{row[self.PRESSURE]}\n" for row in data
        ]

        # Store the data
        try:
            with open(save_path, "w") as f:
                f.writelines(f"{meta_data.get('samples_count')}\n")
                f.writelines(data)
                self.log(f"Data stored in {save_path}")

        except Exception:
            self.log(f"Unable to store the file {save_path}")
            raise

    # ------------------ #
    # Validation methods #
    # ------------------ #

    @classmethod
    def validate_data(cls, df_data):
        """Validates output data (already in pandas DataFrame)"""
        return SampleRead.validate_data(df_data)

    # --------------- #
    # Utility methods #
    # --------------- #

    def _prepare_meta_data(self, meta_data=None):
        """Prepares the meta data before storing"""

        # Handle no meta data
        meta_data = meta_data if meta_data else {}

        # Create or update the timestamps
        meta_data["written_on"] = datetime.utcnow().strftime(self.DATE_FORMAT)
        meta_data["created_on"] = datetime.utcnow().strftime(self.DATE_FORMAT) \
            if not meta_data.get("created_on", None) \
            else meta_data.get("created_on", None)

        # Return the prepared meta data
        return meta_data

    @staticmethod
    def _collect_file_name(meta_data):
        """Collects information from meta data and creates a filename"""

        # Handle "old" data
        if meta_data.get("participant", None) is None:
            raise ValueError(f"No proper meta data for this sample, please select filename manually")

        # Collect the information
        participant_id = meta_data.get("participant", {}).get("id", None)
        birth_date = meta_data.get("participant", {}).get("birth_date", None)
        sex = meta_data.get("participant", {}).get("sex", None)
        task_id = meta_data.get("task_id", None)
        admin = meta_data.get("administrator", None)
        created_on = meta_data.get("created_on", None)

        # Return the filename
        return f"{participant_id}_{birth_date}_{sex}_{task_id}_{admin}_{created_on}"
