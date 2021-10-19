from sample.sample import Sample
from sample.transformers import Transformer

additional_meta_data = {
    "column_names": [Sample.TILT, Sample.AZIMUTH, Sample.AX_X, Sample.PRESSURE, Sample.PEN_STATUS, Sample.TIME, Sample.AX_Y],
    "protocol_id": "pd_protocol_2018",
    "device_type": "Wacom Cinitq",
    "device_driver": "2.1.0",
    "wintab_version": "1.2.5",
    "lpi": 1024,
    "time_series_ranges": {
      "x": [0, 1025],
      "y": [0, 1056],
      "azimuth": [0, 1000],
      "tilt": [0, 1000],
      "pressure": [0, 2048]
    }
}

test_file = "jack_18-07-2014_M_0006_Doe_12-10-2020.json"


def test_normalize_time_series():
    sample = Sample(data_source=test_file)
    print(sample._data)
    print(Transformer.normalize_time_series(sample.x, 1056))
    assert sample


def test_transform_axis():
    sample = Sample(data_source=test_file)
    print(sample._data)
    print(Transformer.transform_axis(sample._data))
    assert sample


def test_transform_time():
    sample = Sample(data_source=test_file)
    print(sample._data)
    print(Transformer.transform_time_to_seconds(sample.time))
    assert sample


def test_transform_angle():
    sample = Sample(data_source=test_file)
    print(sample._data)
    transformed_angle = Transformer.transform_angle(sample.tilt, Transformer.MAX_TILT_VALUE, Transformer.MAX_TILT_DEGREE)
    print(transformed_angle)

    transformed_angle = Transformer.transform_angle(sample.azimuth, Transformer.MAX_AZIMUTH_VALUE, Transformer.MAX_AZIMUTH_DEGREE)
    print(transformed_angle)

    assert sample


def test_normalize_pressure():
    sample = Sample(data_source=test_file)
    print(sample._data)
    normalized_pressure = Transformer.normalize_pressure(sample.pressure)
    print(normalized_pressure)

    assert sample


def test_transform_handwriting_units():
    sample = Sample(data_source=test_file)
    print(sample._data)

    sample = Transformer.transform_handwriting_units(sample)
    print(sample.x)
    print(sample.y)
    print(sample.time)
    print(sample.azimuth)
    print(sample.tilt)
    print(sample.pressure)

    assert sample


def test_control_for_pressure():
    sample = Sample(data_source=test_file)
    print(sample._data)

    sample.pressure = Transformer.control_for_pressure(sample.pressure)

    assert sample
