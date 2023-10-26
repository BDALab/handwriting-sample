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
    MM = "mm"

    # Define device defaults (DTK-1660)
    LPI_VALUE = 5080
    LPMM_VALUE = 200
    MM_VALUE = 0.01
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
        :param max_value: max heoretical value
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
        :param max_value: OPTIONAL, DEFAULT = 32767
                          max theoretical raw pressure value
        :type max_value: int
        :param pressure_levels: OPTIONAL, DEFAULT = 8192
                                level of pressure of the device
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

    def transform_axis(self, sample, conversion_type=LPI, lpi_value=LPI_VALUE, lpmm_value=LPMM_VALUE,
                       shift_to_zero=True):
        """
        Transforms X,Y axis to millimeters.

        :param sample: object of HandwritingSample class
        :type sample: handwriting_sample.HandwritingSample
        :param conversion_type: OPTIONAL ["lpi"|"lpmm"|"mm"], DEFAULT="lpi".
                                Set the capturing method used for mapping;
                                "lpi" for inch; "lpmm" for millimeters;
                                "mm" for direct to millimeters
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
        :return: updated object of HandwritingSample class
        :rtype: handwriting_sample.HandwritingSample
        """

        # Check input
        if not isinstance(conversion_type, str):
            raise ValueError(f"Conversion type must be string not {type(conversion_type)}.")
        if not isinstance(lpi_value, int):
            raise ValueError(f"LPI value must be int not {type(lpi_value)}.")
        if not isinstance(lpmm_value, int):
            raise ValueError(f"LPMM value must be int not {type(lpmm_value)}.")

        # Check for conversion type
        if conversion_type == self.LPI:

            self.log(f"Using {conversion_type} = {lpi_value} for axis conversion to millimeters.")

            # Convert axis
            sample.x = (sample.x * self.INCH_TO_MM) / lpi_value
            sample.y = (sample.y * self.INCH_TO_MM) / lpi_value

        # BAD FORMULA... MAKING NO SENSE!
        # elif conversion_type == self.LPMM:
        #
        #     self.log(f"Using {conversion_type} = {lpmm_value} for axis conversion to millimeters.")
        #
        #     # Convert axis
        #     sample.x = (sample.x * self.INCH_TO_MM) / lpmm_value
        #     sample.y = (sample.y * self.INCH_TO_MM) / lpmm_value
        elif conversion_type == self.LPMM:
            raise NotImplementedError(f"Do not supporting this conversion anymore, due to incorrect formula.")

        elif conversion_type == self.MM:

            self.log(f"Using {conversion_type} = {self.MM_VALUE} for axis conversion to millimeters.")

            # Convert axis
            sample.x = sample.x * self.MM_VALUE
            sample.y = sample.y * self.MM_VALUE

        else:
            raise ValueError(f"Unknown conversion type {conversion_type}")

        if shift_to_zero:
            self.log(f"Shift axis data to start from 0,0 coordinates")
            sample.x = sample.x - min(sample.x)
            sample.y = sample.y - min(sample.y)

        return sample

    def transform_all_units(
            self,
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
        Transforms all unites of sample object:
            - transforms X,Y to millimeters.
            - transform time to seconds
            - normalize or transform to degrees angles
            - normalize pressure

        :param sample: updated object of HandwritingSample class
        :type sample: handwriting_sample.HandwritingSample
        :param conversion_type: OPTIONAL ["lpi"|"lpmm"|"mm"], DEFAULT="lpi".
                                Set the capturing method used for mapping;
                                "lpi" for inch; "lpmm" for millimeters;
                                "mm" for direct to millimeters
        :type conversion_type: str
        :param lpi_value:  OPTIONAL , DEFAULT = 5080
                           Set lpi value of digitizing tablet.
        :type lpi_value: int
        :param lpmm_value: OPTIONAL, DEFAULT = 200
                           Set lpmm value of digitizing tablet.
        :type lpmm_value: int
        :param max_raw_azimuth: OPTIONAL, DEFAULT = 3600
                                Maximum theoretical value of azimuth.
        :type max_raw_azimuth: int
        :param max_raw_tilt: OPTIONAL, DEFAULT = 900
                            Maximum theoretical value of tilt.
        :type max_raw_tilt: int
        :param max_degree_azimuth: OPTIONAL, DEFAULT = 360
                                   Maximum degree value of azimuth.
        :type max_degree_azimuth: int
        :param max_degree_tilt: OPTIONAL, DEFAULT = 90
                                Maximum degree value of tilt.
        :type max_degree_tilt: int
        :param max_pressure: OPTIONAL, DEFAULT = 32767
                             Maximum theoretical value of pressure.
        :type max_pressure: int
        :param pressure_levels: OPTIONAL, DEFAULT = 8192
                                Level of pressures of the device.
        :type pressure_levels: int
        :param angles_to_degrees: OPTIONAL, DEFAULT = True
                                  Transform angles to degrees
        :type angles_to_degrees: bool
        :param shift_to_zero: OPTIONAL, DEFAULT = True
                              Shift axis values to start from 0,0 coordinates
        :type shift_to_zero: bool
        :return: updated object of HandwritingSample class
        :rtype: handwriting_sample.HandwritingSample
        """

        # TODO _read max/range values from metadata

        sample = self.transform_axis(
            sample,
            conversion_type=conversion_type,
            lpi_value=lpi_value,
            lpmm_value=lpmm_value,
            shift_to_zero=shift_to_zero)

        # Transform time to seconds
        sample.time = self.transform_time_to_seconds(sample.time)

        # Normalize Azimuth, Tilt or transform to degree
        if angles_to_degrees:

            # Transform to degrees
            sample.azimuth = self.transform_angle(
                sample.azimuth,
                max_raw_azimuth,
                max_degree_azimuth)
            sample.tilt = self.transform_angle(
                sample.tilt,
                max_raw_tilt,
                max_degree_tilt)

        # Normalize pressure
        sample.pressure = self.normalize_pressure(
            sample.pressure,
            max_value=max_pressure,
            pressure_levels=pressure_levels)

        # Return
        return sample

    def control_for_pressure(
            self,
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
        self.log(f"Pressure range of data is: {data_pressure_range}")

        if data_pressure_range > max_range_press:

            # Convert the pressure to lower range
            self.log(f"Maximum allowed pressure range is: {max_range_press}.")
            self.log(f"Converting pressure values with following params:")
            self.log(f"  - device max pressure level = {pressure_levels}")
            self.log(f"  - raw data max pressure value = {max_raw_press_value}")

            output = np.array(list(map(lambda x: round((x / max_raw_press_value) * max_range_press), input_array)))
            print(f"Converted Pressure range is: {np.ptp(output)}")

            return output
        return input_array

    @staticmethod
    def correct_pen_status(sample):
        """
        Corrects pen status values to binary form

        :param sample: updated object of HandwritingSample class
        :type sample: handwriting_sample.HandwritingSample
        :return: instance of HandwritingSample
        :rtype: HandwritingSample
        """

        # Correct pen status
        sample.pen_status = np.array(list(map(lambda x: 1 if x > 0 else 0, sample.pressure)))

        # Hold meta data
        meta_data = sample.meta

        # Validate sample and return
        r_sample = sample.from_pandas_dataframe(sample.data_pandas_dataframe)

        # Put back teh meta data
        r_sample.add_meta_data(meta_data)

        return r_sample

    @staticmethod
    def revert_axis(input_array, axis_max_value):
        """
        Revert axis

        :param input_array: Input array with raw angle values
        :type input_array: np.array
        :return: reverted axis
        :rtype: nd.array
        """

        # Check input
        if not all(isinstance(x.item(), (int, float)) for x in input_array):
            raise ValueError(f"Input data are not numbers!")
        if not isinstance(axis_max_value, (int, float)):
            raise ValueError(f"Axis max value is not a number!")
        if max(input_array) > axis_max_value:
            raise ValueError(f"Axis max value ({axis_max_value}) is lower than max value of the input array"
                             f" ({max(input_array)})! ")
        # Revert axis
        return np.array(list(map(lambda x: axis_max_value - x, input_array)))

    @staticmethod
    def rescale_axis(sample, rescale_coef=0.5):
        """
        Rescale axis values

        :param sample: updated object of HandwritingSample class
        :type sample: handwriting_sample.HandwritingSample
        :param rescale_coef: OPTIONAL - Coefficient of rescaling, DEFAULT = 0.5
        :type rescale_coef: float
        :return: handwriting sample with rescaled axis
        :rtype: handwriting_sample.HandwritingSample
        """

        # Check input
        if not isinstance(rescale_coef, (int, float)):
            raise ValueError(f"Coefficient of rescaling is not number!")

        sample.x = sample.x * rescale_coef
        sample.y = sample.y * rescale_coef

        return sample

    @staticmethod
    def transform_tilt_xy_to_azimuth_and_tilt(tilt_x, tilt_y):
        """
        Transforms tiltX and tiltY to azimuth and tilt

        :param tilt_x: tiltX values in degrees
        :type tilt_x: np.array
        :param tilt_y: tiltY values in degrees
        :type tilt_y: np.array
        :return: azimuth and tilt in degrees
        :rtype: np.array, np.array
        """

        azimuth = np.zeros(len(tilt_x))
        tilt = np.zeros(len(tilt_x))
        idx = 0

        for t_x, t_y in zip(tilt_x, tilt_y):
            t_x = np.radians(t_x)
            t_y = np.radians(t_y)

            # if both TiltX and TiltY = 0 then azimuth = 0 and tilt = pi/ 2
            if t_x == 0 and t_y == 0:
                azimuth[idx] = 0
                tilt[idx] = (np.pi / 2)

            # if TiltX = 0 and TiltY > 0 then azimuth = pi/ 2 and tilt = pi/ 2-TiltY
            elif t_x == 0 and t_y > 0:
                azimuth[idx] = (np.pi / 2)
                tilt[idx] = (np.pi / 2) - t_y

            # if TiltX = 0 and TiltY < 0 then azimuth = 3 * pi/ 2 and tilt = pi/ 2+TiltY
            elif t_x == 0 and t_y < 0:
                azimuth[idx] = (3 * (np.pi / 2))
                tilt[idx] = (np.pi / 2) + t_y

            # if TiltY = 0 and TiltX > 0 then azimuth = 0 and tilt = pi/ 2-TiltX
            elif t_x > 0 and t_y == 0:
                azimuth[idx] = 0
                tilt[idx] = (np.pi / 2) - t_x

            # if TiltY = 0 and TiltX < 0 then azimuth = pi and tilt = pi/ 2+TiltX
            elif t_x < 0 and t_y == 0:
                azimuth[idx] = np.pi
                tilt[idx] = (np.pi / 2) + t_x

            # All other cases
            else:
                azimuth[idx] = np.arctan(np.tan(t_y) / np.tan(t_x))
                tilt[idx] = np.arctan(np.sin(azimuth[idx]) / np.tan(t_y))

            idx += 1

        # Transform to degrees
        azimuth = np.degrees(azimuth)
        tilt = np.degrees(tilt)

        return azimuth, tilt

