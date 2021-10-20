from examples.tests.common_test_data import *
from handwriting_sample.transformers import Transformer


def test_normalize_time_series():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)
    print(sample._data)
    print(Transformer.normalize_time_series(sample.x, 1056))
    assert sample


def test_transform_axis():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)
    print(sample._data)
    print(Transformer.transform_axis(sample._data))
    assert sample


def test_transform_time():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)
    print(sample._data)
    print(Transformer.transform_time_to_seconds(sample.time))
    assert sample


def test_transform_angle():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)
    print(sample._data)
    transformed_angle = Transformer.transform_angle(sample.tilt, Transformer.MAX_TILT_VALUE, Transformer.MAX_TILT_DEGREE)
    print(transformed_angle)

    transformed_angle = Transformer.transform_angle(sample.azimuth, Transformer.MAX_AZIMUTH_VALUE, Transformer.MAX_AZIMUTH_DEGREE)
    print(transformed_angle)

    assert sample


def test_normalize_pressure():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)
    print(sample._data)
    normalized_pressure = Transformer.normalize_pressure(sample.pressure)
    print(normalized_pressure)

    assert sample


def test_transform_handwriting_units():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)
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
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)
    print(sample._data)

    sample.pressure = Transformer.control_for_pressure(sample.pressure)

    assert sample
