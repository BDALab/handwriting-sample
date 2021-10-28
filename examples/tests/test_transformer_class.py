from examples.tests.common_test_data import *
from handwriting_sample.transformer import HandwritingSampleTransformer


def test_normalize_time_series():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)

    print(HandwritingSampleTransformer.normalize_time_series(sample.x, 1056))
    assert sample


def test_transform_axis():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)

    print(HandwritingSampleTransformer.transform_axis(sample))
    assert sample


def test_transform_time():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)

    print(HandwritingSampleTransformer.transform_time_to_seconds(sample.time))
    assert sample


def test_transform_angle():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)

    transformed_angle = HandwritingSampleTransformer.transform_angle(
        sample.tilt,
        HandwritingSampleTransformer.MAX_TILT_VALUE,
        HandwritingSampleTransformer.MAX_TILT_DEGREE)
    print(transformed_angle)

    transformed_angle = HandwritingSampleTransformer.transform_angle(
        sample.azimuth,
        HandwritingSampleTransformer.MAX_AZIMUTH_VALUE,
        HandwritingSampleTransformer.MAX_AZIMUTH_DEGREE)
    print(transformed_angle)

    assert sample


def test_normalize_pressure():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)

    normalized_pressure = HandwritingSampleTransformer.normalize_pressure(sample.pressure)
    print(normalized_pressure)

    assert sample


def test_transform_handwriting_units():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)

    sample = HandwritingSampleTransformer.transform_all_units(sample)
    print(sample.x)
    print(sample.y)
    print(sample.time)
    print(sample.azimuth)
    print(sample.tilt)
    print(sample.pressure)

    assert sample


def test_control_for_pressure():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)

    sample.pressure = HandwritingSampleTransformer.control_for_pressure(sample.pressure)

    assert sample
