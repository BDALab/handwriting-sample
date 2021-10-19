import numpy as np
from sample.sample import Sample
from sample.transformers import Transformer

from pprint import pprint

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


def test_read_sample_svc():

    sample = Sample.from_svc("../svc_data/signal.svc")
    print(sample)
    print(sample.time)

    assert sample


def test_read_sample_svc_new():
    column_names = ['x', 'y', 'time', 'pen_status', 'azimuth', 'tilt', 'pressure']

    sample = Sample.from_svc("../svc_data/jack_18-07-2014_M_0006_Doe_12-10-2020.svc", column_names=column_names)
    pprint(sample.meta_data)
    sample.add_meta_data(additional_meta_data)
    pprint(sample.meta_data)
    print(sample._data)

    assert sample


def test_read_sample_json():
    sample = Sample.from_json("../json_data/signal.json")
    print(sample)

    assert sample


def test_read_sample_pandas():
    # get _data in pd.Dataframe
    sample = Sample.from_json("../json_data/signal.json")
    data_df = sample._data

    # Reorder _data (to check if ordering is working)
    data_df = data_df[[Sample.TILT, Sample.AZIMUTH, Sample.AX_X, Sample.PRESSURE, Sample.PEN_STATUS, Sample.TIME, Sample.AX_Y]]

    # Read _data from DataFrame
    df_sample = Sample.from_pandas(data_df)
    print(df_sample._data)

    assert df_sample


def test_from_array():
    array = np.array([[1,1,1,1,1],
                      [1,2,3,4,5],
                      [1,20,30,40,50],
                      [1,2,3,4,5],
                      [1,2,3,4,5],
                      [1,2,3,4,5],
                      [1,2,3,4,5]])

    column_names = ['pen_status', 'y', 'x', 'time', 'azimuth', 'tilt', 'pressure']

    sample = Sample.from_array(array, column_names=column_names)
    print(sample)

    assert sample


def test_validate_sample_pandas():
    # get _data in pd.Dataframe
    sample = Sample.from_json("../json_data/signal.json")
    data_df = sample._data

    # Drop column
    # data_df = data_df.drop(columns=[Sample.TIME, Sample.AX_X])

    # # Add columns
    # data_df['Biceps'] = 1
    # data_df['HeadDiameter'] = 1
    #
    # # Set column to null
    data_df['time'] = None

    # Read corrupted _data
    df_sample = Sample.from_pandas(data_df)

    print(df_sample)


def test_read_sample_array():
    sample = Sample.from_svc("../svc_data/signal.svc")
    print(sample._data)
    print(f"X: {sample.x}")
    print(f"Time: {sample.time}")

    assert sample


def test_split_movements():
    sample = Sample.from_svc("../svc_data/jack_18-07-2014_M_0006_Doe_12-10-2020.svc")

    on_surface_data = sample.get_on_surface_data()
    print(f"On Surface: {on_surface_data}")

    in_air_data = sample.get_in_air_data()
    print(f"In Air: {in_air_data}")

    assert sample


def test_get_strokes():
    sample = Sample.from_svc("../svc_data/jack_18-07-2014_M_0006_Doe_12-10-2020.svc")
    strokes = sample.get_strokes()
    print(f"Number of strokes: {len(strokes)}")

    assert sample


def test_get_on_surface_strokes():
    sample = Sample.from_svc("../svc_data/jack_18-07-2014_M_0006_Doe_12-10-2020.svc")
    strokes = sample.get_on_surface_strokes()
    print(f"Number of strokes on surface: {len(strokes)}")

    assert sample


def test_get_in_air_strokes():
    sample = Sample.from_svc("../svc_data/jack_18-07-2014_M_0006_Doe_12-10-2020.svc")
    strokes = sample.get_in_air_strokes()
    print(f"Number of strokes in air: {len(strokes)}")

    assert sample


def test_store_data():
    # sample = Sample(data_source="signal.json")
    sample = Sample.from_svc("../svc_data/jack_18-07-2014_M_0006_Doe_12-10-2020.svc")

    sample.to_json("./")

    assert sample


def test_store_raw_data():
    # sample = Sample(data_source="signal.json")
    sample = Sample.from_svc("../svc_data/jack_18-07-2014_M_0006_Doe_12-10-2020.svc")

    sample.to_svc("./", original_data=True, file_name="original_data")

    assert sample


def test_load_sample_with_transformation():

    sample = Sample.from_svc("../svc_data/jack_18-07-2014_M_0006_Doe_12-10-2020.svc")
    # print(sample)

    sample = Transformer.transform_handwriting_units(sample, angles_to_degrees=True)
    print(f"X: {sample.x}")
    print(f"Time: {sample.time}")

    sample.to_svc("./", file_name="data_tr")
    sample.to_svc("./", original_data=True, file_name="original_data_tr")

    assert sample