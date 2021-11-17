from handwriting_sample.base import HandwritingDataBase


class HandwritingSampleValidator(HandwritingDataBase):
    """Class implementing handwriting data validator"""

    # ------------------ #
    # Validation methods #
    # ------------------ #
    # TODO: idea: make library specific exceptions

    @classmethod
    def validate_data(cls, df_data):
        """Validates input data"""

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

        # Check if pen status contain only 0,1 values
        for index, value in enumerate(df_data[cls.PEN_STATUS]):
            if value not in [0, 1]:
                raise ValueError(f"Pen status contain data different from [0,1]. "
                                 f"Check value: `{value}` on line {index}")

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
