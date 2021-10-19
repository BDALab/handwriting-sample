import os
import json
import pandas as pd

from sample.base import Base


class SampleRead(Base):
    """
    Class reading and validating input data
    """

    def __init__(self, column_names):
        """ Init SampleRead object and map of read functions

        :param column_names: ordered names of the dataframe column
        :type column_names: list
        """

        # Define column names
        self.column_names = column_names

    def read_from_json(self, data_path):
        """
        Read data from the JSON file

        :return: Raw data in dict
        :rtype: dict
        """

        # Open JSON
        with open(data_path, 'r') as file:
            json_data = json.load(file)
        # # Load data part to pandas
        # df_data = pd.DataFrame.from_dict(json_data.get('data'))
        data = json_data.get('data')
        self.log(f"Data has been loaded from: {data_path}.")

        # Load meta_data part to dict
        meta_data = json_data.get('meta_data')

        # return data and meta_data
        return data, meta_data

    def read_from_svc(self, data_path, column_names=None):
        """
        Read data from the SVC file

        :return: Raw data in dict
        :rtype: dict
        """

        # Read column names from input
        if column_names:
            self.column_names = column_names

        # Read data (skip first row with meta data)
        data = pd.read_csv(data_path, sep=' ', names=self.column_names, skiprows=1).to_dict(orient='list')
        self.log(f"Data has been loaded from: {data_path}.")

        # return data and meta_data
        return data, self._read_metadata_from_svc_file_name(data_path)

    def read_from_array(self, array_data, column_names=None):
        """
        Read data from the SVC file

        :return: Raw data in dict
        :rtype: dict
        """

        # Read column names from input
        if column_names:
            self.column_names = column_names

        # Prepare dict from input array and column names
        data = {}
        for key, val in zip(self.column_names, array_data):
            data[key] = val

        return data

    def _remove_first_in_air_data(self, df_data):
        """
        Check if data contains not wanted in-air movement at the beginning of the writing and remove them

        :param df_data: Input data frame
        :type: pd.Dataframe
        """

        self.log(f"Check if data contains first in air movement (not wanted one, before the writing)")

        # Check if first sample has in air movement
        if df_data['pen_status'].iloc[0] == 1:
            # If no, continue
            self.log(f"Data do not contains IN-AIR movement at the beginning. Let's continue.")
            return

        self.log(f"Data contains IN-AIR movement at the beginning. Let's remove them.")
        # Iterate over rows
        count = 0
        for index, row in df_data.iterrows():
            # Chek if movement is in-air
            if row['pen_status'] == 0:
                # Remove it
                df_data.drop(index, inplace=True)
                count += 1
            else:
                # Else break (We need to remove only the first one)
                self.log(f"We removed {count} first in air samples.")
                # Reset index to begin from 0
                df_data.reset_index(inplace=True)
                return

    def _remove_last_in_air_data(self, df_data):
        """
        Check if data contains not wanted in-air movement at the end of the writing and remove them

        :param df_data: Input data frame
        :type: pd.Dataframe
        """

        self.log(f"Check if data contains last in air movement (not wanted one, after the writing)")

        # Check if last sample has in air movement
        if df_data['pen_status'].iloc[-1] == 1:
            # If no, continue
            self.log(f"Data do not contains IN-AIR movement at the end. Let's continue.")
            return

        self.log(f"Data contains IN-AIR movement at the end. Let's remove them.")

        # Loop through rows of dataframe by index in reverse i.e. from last row to row at 0th index.
        # Check for in-air movement at the end of the data and remove it
        count = 0
        for index in range(df_data.shape[0] - 1, -1, -1):
            # get row contents as series using iloc{] and index position of row
            if df_data['pen_status'].iloc[index] == 0:
                # Remove it
                df_data.drop(index, inplace=True)
                count += 1
            else:
                # Else break (We need to remove only the last one)
                self.log(f"We removed {count} last in air samples.")
                # Reset index to begin from 0
                df_data.reset_index(inplace=True)
                return

    def _remove_first_last_in_air_data(self, df_data):
        """
        Check if data contains not wanted in-air movement and remove them

        :param df_data: Input data frame
        :type: pd.Dataframe
        """

        self._remove_first_in_air_data(df_data)
        self._remove_last_in_air_data(df_data)

    def validate_data(self, df_data):
        """
        Method to validate the input data (already in DataFrame)

        :param df_data: Input data
        :type df_data: pd.DataFrame

        :return: Validated input data with ordered columns
        :rtype: pd.DataFrame
        """

        # Set column names to lower case
        df_data.columns = [x.lower() for x in df_data.columns]

        # Get column count
        columns = df_data.columns

        # Check for number of time-series
        if len(columns) < len(self.column_names):
            # get missing columns
            missing_columns = list(set(columns).symmetric_difference(set(self.column_names)))

            raise ValueError(f"Input data are missing following time-series: {missing_columns}")

        if len(columns) > len(self.column_names):
            # Get additional columns
            additional_columns = list(set(columns).symmetric_difference(set(self.column_names)))

            raise ValueError(f"Too much data on Input. Please remove following columns: {additional_columns}")

        # Check for missing values:
        if df_data.isnull().sum().sum() > 0:
            # Print overview of emtpy values
            null_overview = df_data.isnull().sum()

            raise ValueError(f"Empty values in input data! Please inspect your input and replace the emtpy values. \n"
                             f"Following table shows count of emtpy values in particular columns: \n{null_overview}.")

        # Check if values are numbers
        for column_name in columns:
            if not all(isinstance(x, (int, float)) for x in df_data[column_name]):
                raise ValueError(f"Datatype in time-series [\'{column_name}\'] are not numbers! ")

        # Order columns based on Default
        df_data = df_data[self.column_names]

        # Remove first in-air data if any
        self._remove_first_last_in_air_data(df_data)

        # TODO Validate data on data range from configuration

        return df_data

    def _read_metadata_from_svc_file_name(self, file_path):
        """
        Process meta data included in the file

        :param file_path: Path to the data file
        :type file_path: str

        :return: a dictionary with file meta data
        :rtype: dict
        """

        # Prepare meta data
        meta_data = {}

        # Open file and _read first line
        with open(file_path) as f:
            raw_meta_data = f.readline()

        # Store samples count
        meta_data["samples_count"] = int(raw_meta_data)

        # Get only file name and split it to get meta data from it
        file_path = os.path.basename(os.path.splitext(file_path)[0])
        meta_from_file_name = file_path.split('_')

        # This may seem strange but there are 2 optional info
        # which can be included in file name (HandAQUS), so let's handle it
        if len(meta_from_file_name) >= 4:
            # If there exist all mandatory 4 meta info store them all
            meta_data["participant"] = {"id": meta_from_file_name[0]}
            meta_data["created_on"] = meta_from_file_name[-1]
            meta_data["administrator"] = meta_from_file_name[-2]
            meta_data["task_id"] = meta_from_file_name[-3]

            if len(meta_from_file_name) == 6:
                # If there exist 6 meta info store the two optional
                meta_data["participant"] = {"id": meta_from_file_name[0],
                                            "birth_date": meta_from_file_name[1],
                                            "sex": meta_from_file_name[2]
                                            }
        else:
            self.log("WARNING: Old file-name format no additional meta data")

        # Return meta data
        return meta_data