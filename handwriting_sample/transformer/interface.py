import numpy as np
from handwriting_sample.base import HandwritingDataBase


class HandwritingSampleTransformer(HandwritingDataBase):
    """Class implementing handwriting data transformer"""

    # Define conversion variables
    INCH_TO_MM = 25.4
    CM_TO_MM = 10

    # Define conversion types
    LPI = "lpi"
    LPMM = "lpmm"

    # Define device defaults (DTK-1660)
    LPI_VALUE = 5080
    LPMM_VALUE = 200
    MAX_PRESSURE_VALUE = 32767
    PRESSURE_LEVELS = 8192
    MAX_TILT_VALUE = 900
    MAX_AZIMUTH_VALUE = 3600

    MAX_TILT_DEGREE = 90
    MAX_AZIMUTH_DEGREE = 360

    MAX_OLD_RANGE_PRESSURE = 1024

    @staticmethod
    def normalize_time_series(input_array, max_value):
        """
        Normalizes input time-series.

        :param input_array: Array of input data
        :type input_array: nd.array
        :param max_value: maximum theoretical value
        :type max_value: int
        :return: Normalized data
        :rtype: list
        """

        # Check input
        if not all(isinstance(x.item(), (int, float)) for x in input_array):
            raise ValueError(f"Input data are not numbers!")
        if not isinstance(max_value, (int, float)):
            raise ValueError(f"Max value is not number!")

        # Return normalized array
        return np.array(list(map((lambda x: x / max_value), input_array)))

    @staticmethod
    def normalize_pressure(input_array, max_value=MAX_PRESSURE_VALUE, pressure_levels=PRESSURE_LEVELS):
        """
        Normalizes pressure to pressure level of the device.

        :param input_array: Input array with pressure values
        :type input_array: np.array
        :param max_value: maximum theoretical value
        :type max_value: int
        :param pressure_levels: level of pressure of the device
        :type pressure_levels: int
        :return: array with normalized pressure
        :rtype: np.array
        """

        # Check input
        if not all(isinstance(x.item(), (int, float)) for x in input_array):
            raise ValueError(f"Input data are not numbers!")
        if not isinstance(max_value, (int, float)):
            raise ValueError(f"Max value is not number!")
        if not isinstance(pressure_levels, (int, float)):
            raise ValueError(f"Pressure levels is not number!")

        return np.array(list(map((lambda x: (x / max_value) * pressure_levels), input_array)))

    @staticmethod
    def transform_axis(sample, conversion_type=LPI, lpi_value=LPI_VALUE, lpmm_value=LPMM_VALUE, shift_to_zero=True):
        """
        Transforms X,Y axis to millimeters.

        :param sample: object of HandwritingSample class
        :type sample: handwriting_sample.HandwritingSample
        :param conversion_type: OPTIONAL ["lpi"|"lpmm"], DEFAULT="lpi".
                                Set the capturing method used for mapping; "lpi" for inch; "lpmm" for millimeters
        :type conversion_type: str
        :param lpi_value: OPTIONAL, DEFAULT = 5080
                          Set lpi value of digitizing tablet
        :type lpi_value: int
        :param lpmm_value: OPTIONAL, DEFAULT = 200
                           Set lpmm value of digitizing tablet
        :type lpmm_value: int
        :param shift_to_zero: OPTIONAL, DEFAULT = True
                              Shift axis values to start from 0,0 coordinates
        :type shift_to_zero: bool
        :return: Transformed X,Y data
        :rtype: tuple(x,y)
        """

        # Check input
        if not isinstance(conversion_type, str):
            raise ValueError(f"Conversion type must be string not {type(conversion_type)}.")
        if not isinstance(lpi_value, int):
            raise ValueError(f"LPI value must be int not {type(lpi_value)}.")
        if not isinstance(lpmm_value, int):
            raise ValueError(f"LPMM value must be int not {type(lpmm_value)}.")

        # Check for conversion type
        if conversion_type == HandwritingSampleTransformer.LPI:

            HandwritingSampleTransformer().log(f"Using {conversion_type} = {lpi_value} for axis conversion to millimeters.")

            # Convert axis
            sample.x = (sample.x * HandwritingSampleTransformer.INCH_TO_MM) / lpi_value
            sample.y = (sample.y * HandwritingSampleTransformer.INCH_TO_MM) / lpi_value

        elif conversion_type == HandwritingSampleTransformer.LPMM:

            HandwritingSampleTransformer().log(f"Using {conversion_type} = {lpmm_value} for axis conversion to millimeters.")

            # Convert axis
            sample.x = (sample.x * HandwritingSampleTransformer.INCH_TO_MM) / lpmm_value
            sample.y = (sample.y * HandwritingSampleTransformer.INCH_TO_MM) / lpmm_value

        else:
            raise ValueError(f"Unknown conversion type {conversion_type}")

        if shift_to_zero:
            HandwritingSampleTransformer.log(f"Shift axis data to start from 0,0 coordinates")
            sample.x = sample.x - min(sample.x)
            sample.y = sample.y - min(sample.y)

        return sample

    @staticmethod
    def transform_time_to_seconds(time_array):
        """
        Transforms time to seconds.

        :param time_array: input array of timestamp
        :type time_array: np.array
        :return: time in seconds
        :rtype: nd.array
        """

        # Check input
        if not all(isinstance(x.item(), (int, float)) for x in time_array):
            raise ValueError(f"Input data are not numbers!")

        return np.array(list(map((lambda x: (x - time_array[0]) / 1e3), time_array)))

    @staticmethod
    def transform_angle(input_array, max_raw_value, max_degree_value):
        """
        Transforms raw angle to degrees.

        :param input_array: Input array with raw angle values
        :type input_array: np.array
        :param max_raw_value: Maximal theoretical value of raw angle
        :type max_raw_value: int
        :param max_degree_value: Maximal value of angle in degrees
        :type max_degree_value: int
        :return: angle in degrees
        :rtype: nd.array
        """

        # Check input
        if not all(isinstance(x.item(), (int, float)) for x in input_array):
            raise ValueError(f"Input data are not numbers!")
        if not isinstance(max_raw_value, (int, float)):
            raise ValueError(f"Max raw value is not number!")
        if not isinstance(max_degree_value, (int, float)):
            raise ValueError(f"Max angle value is not number!")

        # Get value of degree per one point
        degree_per_point = max_degree_value / max_raw_value

        # Transform array to degrees
        return np.array(list(map((lambda x: (x * degree_per_point)), input_array)))

    @staticmethod
    def transform_all_units(
            sample,
            conversion_type=LPI,
            lpi_value=LPI_VALUE,
            lpmm_value=LPMM_VALUE,
            max_raw_azimuth=MAX_AZIMUTH_VALUE,
            max_raw_tilt=MAX_TILT_VALUE,
            max_degree_azimuth=MAX_AZIMUTH_DEGREE,
            max_degree_tilt=MAX_TILT_DEGREE,
            max_pressure=MAX_PRESSURE_VALUE,
            pressure_levels=PRESSURE_LEVELS,
            angles_to_degrees=True,
            shift_to_zero=True):
        """
        :param sample: object of HandwritingSample class
        :type sample: handwriting_sample.HandwritingSample
        :param conversion_type: OPTIONAL ["lpi"|"lpmm"], DEFAULT="lpi".
                                Set the capturing method used for mapping; "lpi" for inch; "lpmm" for millimeters
        :type conversion_type: str
        :param lpi_value:  OPTIONAL - Set lpi value of digitizing tablet. DEFAULT = 5080
        :type lpi_value: int
        :param lpmm_value: OPTIONAL - Set lpmm value of digitizing tablet. DEFAULT = 200
        :type lpmm_value: int
        :param max_raw_azimuth: OPTIONAL - maximum theoretical value of azimuth. DEFAULT = 3600
        :type max_raw_azimuth: int
        :param max_raw_tilt: OPTIONAL - maximum theoretical value of tilt. DEFAULT = 900
        :type max_raw_tilt: int
        :param max_degree_azimuth: OPTIONAL - maximum degree value of azimuth. DEFAULT = 360
        :type max_degree_azimuth: int
        :param max_degree_tilt: OPTIONAL - maximum degree value of tilt. DEFAULT = 90
        :type max_degree_tilt: int
        :param max_pressure: OPTIONAL - maximum theoretical value of pressure. DEFAULT = 32767
        :type max_pressure: int
        :param pressure_levels: OPTIONAL - level of pressures of the device. DEFAULT = 8192
        :type pressure_levels: int
        :param angles_to_degrees: OPTIONAL, DEFAULT = True
                                  Transform angles to degrees
        :type angles_to_degrees: bool
        :param shift_to_zero: OPTIONAL, DEFAULT = True
                              Shift axis values to start from 0,0 coordinates
        :type shift_to_zero: bool
        :return: HandwritingSample class object with transformed units
        :rtype: handwriting_sample.HandwritingSample
        """

        # TODO _read max/range values from metadata

        sample = HandwritingSampleTransformer.transform_axis(sample, conversion_type=conversion_type, lpi_value=lpi_value,
                                                             lpmm_value=lpmm_value, shift_to_zero=shift_to_zero)

        # Transform time to seconds
        sample.time = HandwritingSampleTransformer.transform_time_to_seconds(sample.time)

        # Normalize Azimuth, Tilt or transform to degree
        if angles_to_degrees:

            # Transform to degrees
            sample.azimuth = HandwritingSampleTransformer.transform_angle(
                sample.azimuth,
                max_raw_azimuth,
                max_degree_azimuth)
            sample.tilt = HandwritingSampleTransformer.transform_angle(
                sample.tilt,
                max_raw_tilt,
                max_degree_tilt)

        # Normalize pressure
        sample.pressure = HandwritingSampleTransformer.normalize_pressure(
            sample.pressure,
            max_value=max_pressure,
            pressure_levels=pressure_levels)

        # Return
        return sample

    @staticmethod
    def control_for_pressure(
            input_array,
            pressure_levels=PRESSURE_LEVELS,
            max_raw_press_value=MAX_PRESSURE_VALUE,
            max_range_press=MAX_OLD_RANGE_PRESSURE):
        """
        Controls for pressure range values.

        This function is a fix pressure function in case the old driver has been used
        Old pressure range is from 0-1024
        New and correct pressure range is 0-32767

        :param input_array: input pressure data
        :type input_array: np.array
        :param pressure_levels: OPTIONAL - level of pressures of the device. DEFAULT = 8192
        :type pressure_levels: int
        :param max_raw_press_value: OPTIONAL - maximum theoretical value of pressure. DEFAULT = 32767
        :type max_raw_press_value: int
        :param max_range_press: OPTIONAL - maximum allowed pressure range of raw data. DEFAULT = 1024
        :type max_range_press: int
        :return: converted pressure to new scale
        :rtype: np.array
        """

        data_pressure_range = np.ptp(input_array)
        HandwritingSampleTransformer().log(f"Pressure range of data is: {data_pressure_range}")

        if data_pressure_range > max_range_press:

            # Convert the pressure to lower range
            HandwritingSampleTransformer().log(f"Maximum allowed pressure range is: {max_range_press}.")
            HandwritingSampleTransformer().log(f"Converting pressure values with following params:")
            HandwritingSampleTransformer().log(f"  - device max pressure level = {pressure_levels}")
            HandwritingSampleTransformer().log(f"  - raw data max pressure value = {max_raw_press_value}")

            output = np.array(list(map(lambda x: round((x / max_raw_press_value) * max_range_press), input_array)))
            print(f"Converted Pressure range is: {np.ptp(output)}")

            return output
        return input_array
