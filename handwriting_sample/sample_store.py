import json
from datetime import datetime
import pandas as pd

from handwriting_sample.base import Base
from handwriting_sample.sample_read import SampleRead


class SampleStore(Base):
    """
    Class storing and validating handwriting data
    """

    def __init__(self):
        """ Init SampleStore object and map of store functions  """

    def store_data(self,
                   data,
                   save_path,
                   to_json=False,
                   to_svc=False,
                   meta_data=None,
                   file_name=None):
        """
        Store sample data

        :param data: input data
        :type data: pd.DataFrame
        :param save_path: Save path
        :type save_path: str
        :param to_json: True if store to json
        :type to_json: bool
        :param to_svc: True if store to svc
        :type to_svc: bool
        :param meta_data: meta data
        :type meta_data: dict
        :param file_name: File name [OPTIONAL if meta data]
        :type file_name: str
        :return:
        """

        # Validate output data
        data = self._validate_output_data(data)

        # If filename is not set create default one:
        if not file_name and meta_data:
            file_name = self._collect_file_name(meta_data)

        # Update save_path
        save_path = f"{save_path}/{file_name}"

        # Create or update time_stamp
        if not meta_data.get('created_on', None):
            meta_data['created_on'] = datetime.utcnow().strftime(self.DATE_FORMAT)

        # Set written on timestamp
        meta_data['written_on'] = datetime.utcnow().strftime(self.DATE_FORMAT)

        if to_json:
            # Transform data to dict (use 'list' variant to get list from each column)
            dict_data = data.to_dict('list')

            self._to_json(dict_data, save_path, meta_data=meta_data)
            return True

        if to_svc:
            # Transform data to dict (use 'record' to get rows)
            dict_data = data.to_dict('r')

            self._to_svc(dict_data, save_path, meta_data=meta_data)
            return True

        self.log(f"Data format not specified.")
        return False

    def _to_json(self,
                 dict_data,
                 save_path,
                 meta_data=None):
        """
        Store sample data to JSON file
        """

        # Create final dict with meta_data
        dict_to_store = {
            "meta_data": meta_data,
            "data": dict_data
        }

        # Update save path
        save_path = f"{save_path}.json"

        try:
            # Store data
            with open(save_path, "w") as json_file:
                json.dump(dict_to_store, json_file)

            self.log(f"Data stored in: {save_path}")

        except Exception as ex:
            self.log(f"Unable to store the file {save_path}.")
            raise Exception(ex)

    def _to_svc(self,
                dict_data,
                save_path,
                meta_data=None):
        """
        Store sample data to SVC file
        """

        # Update save path
        save_path = f"{save_path}.svc"

        try:
            # Store SVC data
            with open(save_path, 'w') as svc_file:
                # Write number of samples
                svc_file.writelines(f"{meta_data.get('samples_count')}\n")
                # Write data
                svc_file.writelines(
                    [f"{row[self.AX_X]} {row[self.AX_Y]} "
                     f"{row[self.TIME]} {row[self.PEN_STATUS]} "
                     f"{row[self.AZIMUTH]} {row[self.TILT]} "
                     f"{row[self.PRESSURE]}\n" for row in dict_data]
                )

            self.log(f"Data stored in: {save_path}")

        except Exception as ex:
            self.log(f"Unable to store the file {save_path}.")
            raise Exception(ex)

    def _marshall(self):
        # TODO prepare Handwriting object for marshalling
        pass

    def _validate_output_data(self, df_data):
        return SampleRead(self.COLUMN_NAMES).validate_data(df_data)

    @staticmethod
    def _collect_file_name(meta_data):
        """
        Collect info from metadata and creates filename

        :return: filename
        :rtype: str
        """
        # If no metadata raise exception (old data)
        if meta_data.get('participant', None) is None:
            raise ValueError(f"No proper meta-data for this sample, please select filename manually.")

        # Collect info
        participant_id = meta_data.get('participant').get('id', None)
        birth_date = meta_data.get('participant').get('birth_date', None)
        sex = meta_data.get('participant').get('sex', None)
        task_id = meta_data.get('task_id', None)
        admin = meta_data.get('administrator', None)
        created_on = meta_data.get('created_on', None)

        return f"{participant_id}_{birth_date}_{sex}_{task_id}_{admin}_{created_on}"

