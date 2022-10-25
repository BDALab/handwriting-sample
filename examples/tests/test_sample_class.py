import numpy as np
from pprint import pprint
from examples.tests.common_test_data import *
from handwriting_sample.validator.exceptions import PenStatusException, NegativeValueException


def test_read_sample_svc():

    sample = HandwritingSample.from_svc(svc_file)
    print(sample)

    assert sample


def test_read_sample_svc_and_add_meta_data():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)
    print("original metadata: ")
    pprint(sample.meta)

    sample.add_meta_data(additional_meta_data)
    print("\n\nnew metadata: ")
    pprint(sample.meta)

    assert sample


def test_read_sample_json():
    sample = HandwritingSample.from_json(json_file)
    print(sample)

    assert sample


def test_read_sample_pandas_with_different_column_order():
    # get _data in pd.Dataframe
    sample = HandwritingSample.from_json(json_file)
    data_df = sample._data

    # Reorder _data (to check if ordering is working)
    data_df = data_df[[HandwritingSample.TILT, HandwritingSample.AZIMUTH,
                       HandwritingSample.AXIS_X, HandwritingSample.PRESSURE,
                       HandwritingSample.PEN_STATUS, HandwritingSample.TIME,
                       HandwritingSample.AXIS_Y]]

    # Read _data from DataFrame
    df_sample = HandwritingSample.from_pandas_dataframe(data_df)
    print(df_sample._data)

    assert df_sample


def test_from_array():
    array = np.array([[1,1,0,1,0],
                      [1,2,3,4,5],
                      [1,20,30,40,50],
                      [1,2,3,4,5],
                      [1,2,3,4,5],
                      [1,2,3,4,5],
                      [1,2,3,4,5]])

    column_names = ['pen_status', 'y', 'x', 'time', 'azimuth', 'tilt', 'pressure']

    sample = HandwritingSample.from_list(array, columns=column_names)
    print(sample)

    assert sample


def test_validate_missing_columns():

    # get _data in pd.Dataframe
    sample = HandwritingSample.from_json(json_file)
    data_df = sample.data_pandas_dataframe

    # Drop columns
    data_df = data_df.drop(columns=[HandwritingSample.TIME])

    # Read corrupted _data
    try:
        df_sample = HandwritingSample.from_pandas_dataframe(data_df)
        assert False
    except Exception as ex:
        print(ex)
        assert ex


def test_validate_additional_columns():
    # get _data in pd.Dataframe
    sample = HandwritingSample.from_json(json_file)
    data_df = sample.data_pandas_dataframe

    # Add columns
    data_df['Biceps'] = 1

    # Read corrupted _data
    try:
        df_sample = HandwritingSample.from_pandas_dataframe(data_df)
        assert False
    except Exception as ex:
        print(ex)
        assert ex


def test_validate_time_is_none():
    # get _data in pd.Dataframe
    sample = HandwritingSample.from_json(json_file)
    data_df = sample.data_pandas_dataframe

    # Set column to null
    data_df['time'] = None

    # Read corrupted _data
    try:
        df_sample = HandwritingSample.from_pandas_dataframe(data_df)
        assert False
    except Exception as ex:
        print(ex)
        assert ex


def test_validate_wrong_pen_status():
    # get _data in pd.Dataframe
    sample = HandwritingSample.from_json(json_file)
    data_df = sample.data_pandas_dataframe

    # Set pen_status 0 to 2
    data_df['pen_status'] = data_df['pen_status'].replace(1, 2)

    # Read corrupted _data
    try:
        df_sample = HandwritingSample.from_pandas_dataframe(data_df)
        assert False
    except Exception as ex:
        print(ex)
        assert ex


def test_split_movements():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)

    on_surface_data = sample.get_on_surface_data()
    print(f"On Surface: {on_surface_data}")

    in_air_data = sample.get_in_air_data()
    print(f"In Air: {in_air_data}")

    assert sample


def test_get_strokes():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)
    strokes = sample.get_strokes()
    print(f"Number of strokes: {len(strokes)}")

    assert sample


def test_get_on_surface_strokes():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)
    strokes = sample.get_on_surface_strokes()
    print(f"Number of strokes on surface: {len(strokes)}")

    assert sample


def test_get_in_air_strokes():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)
    strokes = sample.get_in_air_strokes()
    print(f"Number of strokes in air: {len(strokes)}")

    assert sample


def test_store_data_to_json():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)

    sample.to_json(store_path)

    assert sample


def test_store_raw_data_to_svc():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)

    sample.to_svc(store_path, file_name="original_data", store_original_data=True)

    assert sample


def test_transform_axis():

    sample = HandwritingSample.from_svc(svc_file_with_meta_data)

    sample.transform_axis_to_mm()

    print(sample.x, sample.y)

    assert sample


def test_transform_time():

    sample = HandwritingSample.from_svc(svc_file_with_meta_data)

    sample.transform_time_to_seconds()

    print(sample.time)

    assert sample


def test_transform_pressure():

    sample = HandwritingSample.from_svc(svc_file_with_meta_data)

    sample.normalize_pressure()

    print(sample.pressure)

    assert sample


def test_transform_angle():

    sample = HandwritingSample.from_svc(svc_file_with_meta_data)
    try:
        sample.transform_angle_to_degree(angle='triangle')

        print(sample.tilt)
        assert sample

    except Exception as ex:
        print(ex)
        assert ex


def test_load_sample_with_transformation():

    sample = HandwritingSample.from_svc(f"../svc_data/test2.svc")
    sample.plot_on_surface(x_label=f"ORIGINAL", y_label=f"Samples []")
    sample.transform_all_units(conversion_type=sample.transformer.MM, shift_to_zero=True)
    # sample.transform_axis_to_mm(conversion_type=sample.transformer.MM, shift_to_zero=True)
    sample.plot_on_surface()

    print(sample)

    assert sample


def test_plot_on_surface():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)
    sample.transform_all_units()
    sample.plot_on_surface()

    assert sample


def test_plot_in_air():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)
    sample.transform_all_units()
    sample.plot_in_air()

    assert sample


def test_plot_separate():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)
    sample.transform_all_units()
    sample.plot_separate_movements()

    assert sample


def test_plot_strokes():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)
    sample.transform_all_units()
    sample.plot_strokes()

    assert sample


def test_all_data():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)
    sample.transform_all_units()
    sample.plot_all_data()

    assert sample


def test_from_array_correct_pressure():
    array = np.array([[1,2,0,5,0],
                      [1,2,3,4,5],
                      [1,20,30,40,50],
                      [1,2,3,4,5],
                      [1,2,3,4,5],
                      [1,2,3,4,5],
                      [1,2,0,0,1]])

    column_names = ['pen_status', 'y', 'x', 'time', 'azimuth', 'tilt', 'pressure']

    try:
        sample = HandwritingSample.from_list(array, columns=column_names)

    except PenStatusException:
        sample = HandwritingSample.from_list(array, columns=column_names, validate=False)

        sample = sample.transformer.correct_pen_status(sample)

        print(sample)

    assert sample


def test_revert_y_axis():
    sample = HandwritingSample.from_svc(svc_file_with_meta_data)
    sample.plot_on_surface()
    sample.y = sample.transformer.revert_axis(sample.y, 19000)
    sample.plot_on_surface()


def test_negative_values():
    array = np.array([[1,1,0,0,0],
                      [-1,2,3,4,5],
                      [1,20,30,40,50],
                      [1,2,3,4,5],
                      [1,2,3,4,5],
                      [1,-2,-3,-4,-5],
                      [1,2,0,0,1]])

    column_names = ['pen_status', 'y', 'x', 'time', 'azimuth', 'tilt', 'pressure']

    try:
        HandwritingSample.from_list(array, columns=column_names)
        assert False

    except NegativeValueException:
        assert True


def test_rescale_axis():
    sample = HandwritingSample.from_svc(f"../svc_data/test2.svc")
    sample.plot_on_surface(x_label='ORIGINAL')
    sample = sample.transformer.rescale_axis(sample)
    sample.plot_on_surface(x_label='RESCALED')

    assert True

