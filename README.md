# Handwriting Sample 

![GitHub last commit](https://img.shields.io/github/last-commit/BDALab/handwriting-sample)
![GitHub issues](https://img.shields.io/github/issues/BDALab/handwriting-sample)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/BDALab/handwriting-sample)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/handwriting-sample)
![GitHub top language](https://img.shields.io/github/languages/top/BDALab/handwriting-sample)
![PyPI - License](https://img.shields.io/pypi/l/handwriting-sample)

This package provides a [PyPi-installable](https://pypi.org/project/handwriting-sample/) module for the manipulation with the so-called online handwriting data (handwriting with dynamic information in form of the time-series) acquired by Wacom Digitizing Tablets. The package implements `HandwritingSample` class enabling fast and easy handwriting data-object handling. Handwriting data must consists of: x, y, timestamp, pen status, azimuth, tilt, pressure in its raw form (raw data directly from device without any processing or transformations). The main features are:
 - data load with validation (from *.svc, *.json, array or pandas dataframe)
 - unit transformation
 - simple access to particular time-series
 - data storage

The package can be used also for data acquired from any other devices if they satisfied the collection of the above list of time-series. 


**Contents**:
1. [Installation](#Installation)
3. [Data](#Data)
4. [Examples](#Examples)
5. [License](#License)
6. [Contributors](#Contributors)


## Installation

## Data

## Examples

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributors

This package is developed by the members of [Brain Diseases Analysis Laboratory](http://bdalab.utko.feec.vutbr.cz/). For more information, please contact the head of the laboratory Jiri Mekyska <mekyska@vut.cz> or the main developer: Jan Mucha <mucha@vut.cz>.
