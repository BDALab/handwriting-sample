import os
from datetime import datetime
from src.handwriting_sample.base import LoggableObject
from src.handwriting_sample.writer.writers import JSONFileWriter, SVCFileWriter


class HandwritingSampleWriter(LoggableObject):
    """Class implementing handwriting data writer"""

    # --------------- #
    # Writing methods #
    # --------------- #
    # TODO: idea: there is some common functionality in store_... methods that may be taken out into a common method

    def write_to_json(self, sample, save_path, file_name=None, store_original_data=False, verbose=False):
        """
        Stores HandwritingSample data to a JSON file.

        :param sample: instance of handwriting sample
        :type sample: HandwritingSample
        :param save_path: save path
        :type save_path: str
        :param file_name: file name (optional if meta data), defaults to None
        :type file_name: str, optional
        :param store_original_data: store original data, defaults to False
        :type store_original_data: bool, optional
        :param verbose: verbosity of the logging, defaults to False
        :type verbose: bool, optional
        :return: True if stored, False otherwise
        :rtype: bool
        """

        # Get the data and meta data from the handwriting sample
        data = sample.original_data_pandas_dataframe if store_original_data else sample.data_pandas_dataframe
        meta = sample.meta

        # Prepare and validate the data and meta data
        data = sample.validator.validate_data(data, verbose=verbose)
        meta = self._prepare_meta_data(sample, meta)

        # If the filename is not set, create a default one
        if not file_name and meta:
            file_name = self._collect_file_name(meta)

        # Update the save_path
        save_path = os.path.join(save_path, f"{file_name}.json")

        # Prepare the data to be stored
        data = data.to_dict("list")

        # Write the data
        return JSONFileWriter.write(save_path, data, meta=meta, verbose=verbose)

    def write_to_svc(self, sample, save_path, file_name=None, store_original_data=False, verbose=False):
        """
        Stores HandwritingSample data to an SVC file.

        :param sample: instance of handwriting sample
        :type sample: HandwritingSample
        :param save_path: save path
        :type save_path: str
        :param file_name: file name (optional if meta data), defaults to None
        :type file_name: str, optional
        :param store_original_data: store original data, defaults to False
        :type store_original_data: bool, optional
        :param verbose: verbosity of the logging, defaults to False
        :type verbose: bool, optional
        :return: True if stored, False otherwise
        :rtype: bool
        """

        # Get the data and meta data from the handwriting sample
        data = sample.original_data_pandas_dataframe if store_original_data else sample.data_pandas_dataframe
        meta = sample.meta

        # Prepare and validate the data and meta data
        data = sample.validator.validate_data(data)
        meta = self._prepare_meta_data(sample, meta)

        # If the filename is not set, create a default one
        if not file_name and meta:
            file_name = self._collect_file_name(meta)

        # Update the save_path
        save_path = os.path.join(save_path, f"{file_name}.svc")

        # Prepare the data to be stored
        data = data.to_dict("r")
        data = [
            f"{row[sample.AXIS_X]} {row[sample.AXIS_Y]} "
            f"{row[sample.TIME]} {row[sample.PEN_STATUS]} "
            f"{row[sample.AZIMUTH]} {row[sample.TILT]} "
            f"{row[sample.PRESSURE]}\n" for row in data
        ]

        # Write the data
        return SVCFileWriter.write(save_path, data, meta=meta, verbose=verbose)

    # --------------- #
    # Utility methods #
    # --------------- #

    @classmethod
    def _prepare_meta_data(cls, sample, meta_data=None):
        """Prepares the meta data before writing"""

        # Handle no meta data
        meta_data = meta_data if meta_data else {}

        # Create or update the timestamps
        meta_data["written_on"] = datetime.utcnow().strftime(sample.DATE_FORMAT)
        meta_data["created_on"] = datetime.utcnow().strftime(sample.DATE_FORMAT) \
            if not meta_data.get("created_on", None) \
            else meta_data.get("created_on", None)

        # Return the prepared meta data
        return meta_data

    @classmethod
    def _collect_file_name(cls, meta_data):
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
