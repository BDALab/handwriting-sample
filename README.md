# Handwriting Sample 

[comment]: <> (![GitHub last commit]&#40;https://img.shields.io/github/last-commit/BDALab/handwriting-sample&#41;)

[comment]: <> (![GitHub issues]&#40;https://img.shields.io/github/issues/BDALab/handwriting-sample&#41;)

[comment]: <> (![GitHub code size in bytes]&#40;https://img.shields.io/github/languages/code-size/BDALab/handwriting-sample&#41;)

[comment]: <> (![PyPI - Python Version]&#40;https://img.shields.io/pypi/pyversions/handwriting-sample&#41;)

[comment]: <> (![GitHub top language]&#40;https://img.shields.io/github/languages/top/BDALab/handwriting-sample&#41;)

[comment]: <> (![PyPI - License]&#40;https://img.shields.io/pypi/l/handwriting-sample&#41;)

This package provides a [PyPi-installable](https://pypi.org/project/handwriting-sample/) module for the manipulation 
with the so-called online handwriting data (handwriting with dynamic information in form of the time-series) acquired 
by Wacom Digitizing Tablets. The package implements `HandwritingSample` class enabling fast and easy handwriting 
data-object handling. Handwriting data must consists of 7 following time-series: **x, y, timestamp, pen status, 
azimuth, tilt, pressure**. 

Main features:
 - data load with validation
   - *.svc, 
   - *.json, 
   - array 
   - pandas dataframe
 - unit transformation
   - axis from to mm
   - time to seconds
   - angles to degrees
 - simple access and manipulation with time-series
 - data storage

The package can be used also for data acquired from any other devices if they satisfied the collection of the above list of time-series. 

_The full programming sphinx-generated docs can be seen in `docs/`_.

**Contents**:
1. [Installation](#Installation)
2. [Data](#Data)
3. [Examples](#Examples)
4. [License](#License)
5. [Contributors](#Contributors)


## Installation

```
# Clone the repository
git clone https://github.com/BDALab/handwriting-sample.git

# Install packaging utils
pip install --upgrade pip
pip install --upgrade virtualenv

# Change directory
cd handwriting-sample

# Activate virtual environment
# Linux
virtualenv .venv
source .venv/bin/activate

# Windows
virtualenv venv
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt
```

## Data
### Input data

Input data must consist of handwriting data in the form of time-series acquired by Wacom Digitizing Tablet. 
However, other similar devices can be used too, if they satisfy the following data structure:

- ``x``: X axis 
- ``y``: Y axis 
- ``time``: timestamp since epoch
- ``pen_status``: pen up or down (0 = up, 1 = down) 
- ``azimuth``: azimuth of the pen tip
- ``tilt``: tilt of the pen regarding the tablet surface
- ``pressure``: pressure


---
Example of the *.svc database can be found [here](https://bdalab.utko.feec.vutbr.cz/#downloads).

---

### Metadata
To bring more insights for the processed data sample, we support the metadata. Metadata can be read in two forms:
1. (NOT RECOMMENDED) from the file name of SVC file (see [SVC file](#SVC file))
2. from the JSON file, part ``meta_data`` (see [JSON file](#JSON file))
3. from the ``key: value`` dictionary using ``add_meta_data``, once the sample has been loaded 
(see [Examples](#Examples))

### Input data examples
#### SVC file
full SVC example can be found [here](examples/svc_data)

```csv
606 
4034 7509 354642400 1 1190 720 10852
4034 7509 354642408 1 1180 700 10997
4150 7582 354642416 1 1170 690 11061
4241 7639 354642423 1 1150 670 11077
4362 7714 354642431 1 1130 650 12085
4513 7810 354642438 1 1120 640 13222
4693 7926 354642446 1 1110 640 14278
...
```
first line in SVC represents the number of samples (lines) in SVC file

**SVC Metadata**

Metadata are read from the file name with the following convention:

``SubjectID_DateOfBirth_Gender_TaskNumber_AdministratorName_DateOfAcquisition.svc``

example:

ID0025_18-07-2014_M_0007_Doe_12-05-2021.svc

#### JSON file
full JSON example can be found [here](examples/json_data/signal.json)
```json
{
  "meta_data":
  {
    "samples_count": 100,
    "column_names": ["x", "y", "time", "pen_status", "azimuth", "tilt", "pressure"],
    "administrator": "Doe",
    "participant":
    {
      "id": "BD_1234",
      "sex": "female",
      "birth_date": "2002-11-05",
    },
    "task_id": 7,
    ...
  },
  "data":
  {
    "x":
    [
      52.81, 52.83, 52.855, 52.87, 52.88, 52.89, 52.9, ...
    ],
    "y":
    [
      52.81, 52.83, 52.855, 52.87, 52.88, 52.89, 52.9, ...
    ],
    "time":
    [
      0.0, 0.007, 0.015, 0.022, 0.03, 0.037, 0.045, ...
    ],
    "pen_status":
    [
      1, 1, 1, 1, 1, 1, 1, ...
    ],
    
    "azimuth":
    [
      510.0, 510.0, 510.0, 510.0, 510.0, ... 
    ],
    "tilt":
    [
      520.0, 520.0, 520.0, 520.0, 520.0, ...
    ],
    "pressure":
    [
      0.0, 0.01173, 0.022483, 0.035191, 0.056696, ...
    ]
  }
}
```
**JSON Metadata**

Metadata are read from the ``"meta_data"`` section of the JSON file



#### Numpy Array
When loading data using numpy array, ensure the proper identification of the time series order.
```python
array = numpy.array([[1,1,1,1,0],
                      [1,2,3,4,5],
                      [1,2,3,4,5],
                      [254651615,254651616,254651617,254651618,254651619],
                      [1,2,3,4,5],
                      [1,2,3,4,5],
                      [10,20,30,40,50]])

column_names = ['pen_status', 'y', 'x', 'time', 'azimuth', 'tilt', 'pressure']
```

#### Pandas DataFrame

```python
x = [1,2,3,4,5]
y = [1,2,3,4,5]
time = [254651615,254651616,254651617,254651618,254651619]
pen_status = [1,2,3,4,5]
azimuth = [1,2,3,4,5]
tilt= [1,2,3,4,5]
pressure=[10,20,30,40,50]

pandas.DataFrame(numpy.column_stack([x, y, time, pen_status, azimuth, tilt, pressure]))

column_names = ['x', 'y', 'time', 'pen_status', 'azimuth', 'tilt', 'pressure']
```



## Handwriting Unit Transformation
The package supports all data unit transformation:
1. _axis values to mm_: for the axis transformation we need to set a Line-Per-Inch (LPI) or Line-Per-Millimeter (LPMM)
   of 
   the device. This value depends on the device type and RAW 
      data gathering. 
**By default, we are using LPI for conversion**
2. _time to seconds_: from the time since epoch to seconds starting from 0
3. _angles to degree_: for the angle transformation we need to set maximal theoretical value of raw angle range and 
   maximal value of angle in degrees based on device capabilities
4. _pressure normalization_: from the RAW pressure values to pressure levels based on device capabilities

By default, package uses predefined technical values for 
[Wacom Cintiq 16](http://101.wacom.com/UserHelp/en/TOC/DTK-1660.html) tablet:

| Name | Value  |   
|---|---|
| LPI  |  5080 | 
| LPMM |  200 |  
| MAX_PRESSURE_VALUE  |  32767 |  
| PRESSURE_LEVELS  |  8192 |  
| MAX_TILT_VALUE  |  900 |  
| MAX_TILT_DEGREE  |  90 |  
| MAX_AZIMUTH_VALUE  |  3600 |  
| MAX_AZIMUTH_DEGREE  |  360 |  

---
**NOTE** 

In case of unit transformation ensure you used a proper technical values regarding your device 

---


## Examples

### Load sample

```python
from handwriting_sample import HandwritingSample

# load from svc
svc_sample = HandwritingSample.from_svc(path="path_to_svc")
print(svc_sample)
```
### Load sample from JSON and print some time-series
```python
from handwriting_sample import HandwritingSample

# load from json
json_sample = HandwritingSample.from_json(path="path_to_json")
print(json_sample)

# print x 
print(json_sample.x)
# print y
print(json_sample.y)
# print trajectory
print(json_sample.xy)
# print pressure
print(json_sample.pressure)
```

### Strokes 
Stroke is one segment of data between the position change of pen up/down.

Return value for all the following methods is tuple with the identification of the movement and object of the 
``HandwritingSample`` class.  

```python
from handwriting_sample import HandwritingSample

# load sample
sample = HandwritingSample.from_json(path="path_to_json")

# get all strokes
strokes = sample.get_strokes()

# get on surface strokes
stroke_on_surface = sample.get_on_surface_strokes()

# get in air strokes
strokes_in_air = sample.get_in_air_strokes()
```

or you just can get the data on surface or in air
```python
from handwriting_sample import HandwritingSample

# load sample
sample = HandwritingSample.from_json(path="path_to_json")

# get movement on surface
on_surface_data = sample.get_on_surface_data()

# get movement in air
in_air_data = sample.get_in_air_data()
```

### Unit Transformation
```python
from handwriting_sample import HandwritingSample

# load sample
sample = HandwritingSample.from_json(path="path_to_json")

# transform axis
sample.transform_axis_to_mm(conversion_type=HandwritingSample.transformer.LPI,
                            lpi_value=5080,
                            shift_to_zero=True)

# transform time to seconds
sample.transform_time_to_seconds()

# transform angle
sample.transform_angle_to_degree(angle=HandwritingSample.TILT)
```

or you can transform all unit at once
```python
from handwriting_sample import HandwritingSample

# load sample
sample = HandwritingSample.from_json(path="path_to_json")

# transform axis
sample.transform_all_units()
```
### Store Data
If you provide a metadata the filename will be generated automatically, 
otherwise you need to select a filename. 
Moreover, you can also store the original data only.

```python
from handwriting_sample import HandwritingSample

# load sample from svc
sample = HandwritingSample.from_svc(path="path_to_svc")

# store data to json
sample.to_json(path="path_to_storage")

# store original raw data to json
sample.to_json(path="path_to_storage", store_original_data=True)
```

### Transform RAW database to database with transformed units
For example if you have a database of SVC files with RAW data,
and you want to transform handwriting units of all data, add some metadata, 
and store it to JSON.  
```python
from handwriting_sample import HandwritingSample

# Prepare metadata
meta_data = {
               {
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
                    "pressure": [0, 2048]}
                }   
            }               

# Go for each file in file list
for file in file_paths:
   # load sample from svc
   sample = HandwritingSample.from_svc(path=file)
   
   # add metadata
   sample.add_meta_data(meta_data=meta_data)
   
   # transform all units
   sample.transform_all_units()
   
   # store original raw data to json
   sample.to_json(path="path_to_storage")
```

### Data visualisation
Package supports also a visualisations e.g.:
```python
from handwriting_sample import HandwritingSample

# load sample from svc
sample = HandwritingSample.from_svc(path="path_to_svc")

# transform all units
sample.transform_all_units()

# Show separate movements
sample.plot_separate_movements()

# Show in air data
sample.plot_in_air()

# Show all data
sample.plot_all_data()
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributors

This package is developed by the members of [Brain Diseases Analysis Laboratory](http://bdalab.utko.feec.vutbr.cz/). For more information, please contact the head of the laboratory Jiri Mekyska <mekyska@vut.cz> or the main developer: Jan Mucha <mucha@vut.cz>.
