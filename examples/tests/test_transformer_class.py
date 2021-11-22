from examples.tests.common_test_data import *


def test_normalize_time_series():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)

    print(sample.transformer.normalize_time_series(sample.x, 1056))
    assert sample


def test_transform_axis():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)

    print(sample.transformer.transform_axis(sample))
    assert sample


def test_transform_time():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)

    print(sample.transformer.transform_time_to_seconds(sample.time))
    assert sample


def test_transform_angle():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)

    transformed_angle = sample.transformer.transform_angle(
        sample.tilt,
        sample.transformer.MAX_TILT_VALUE,
        sample.transformer.MAX_TILT_DEGREE)
    print(transformed_angle)

    transformed_angle = sample.transformer.transform_angle(
        sample.azimuth,
        sample.transformer.MAX_AZIMUTH_VALUE,
        sample.transformer.MAX_AZIMUTH_DEGREE)
    print(transformed_angle)

    assert sample


def test_normalize_pressure():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)

    normalized_pressure = sample.transformer.normalize_pressure(sample.pressure)
    print(normalized_pressure)

    assert sample


def test_transform_handwriting_units():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)

    sample = sample.transformer.transform_all_units(sample)
    print(sample.x)
    print(sample.y)
    print(sample.time)
    print(sample.azimuth)
    print(sample.tilt)
    print(sample.pressure)

    assert sample


def test_control_for_pressure():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)

    sample.pressure = sample.transformer.control_for_pressure(sample.pressure)

    assert sample
