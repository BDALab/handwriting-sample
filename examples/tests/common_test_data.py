from handwriting_sample.interface import HandwritingSample


svc_file_with_meta_data = "../svc_data/jack_18-07-2014_M_0006_Doe_12-10-2020.svc"
svc_file = "../svc_data/signal.svc"
json_file = "../json_data/signal.json"
store_path = "../"

additional_meta_data = {
    "column_names": [
        HandwritingSample.TILT, HandwritingSample.AZIMUTH,
        HandwritingSample.AXIS_X, HandwritingSample.PRESSURE,
        HandwritingSample.PEN_STATUS, HandwritingSample.TIME,
        HandwritingSample.AXIS_Y
    ],
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