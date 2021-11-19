# handwriting-sample
This python module is for handling the data of so-called online handwriting (handwriting with dynamic information in form of time-series) acquired by Wacom Digitizing Tablets. Module supports data from any Wacom device providing raw data, namely: x, y, timestamp, pen status, azimuth, tilt, pressure. Moreover, any other device providing such data can be used.  

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
