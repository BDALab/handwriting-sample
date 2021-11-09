from examples.tests.common_test_data import *


def test_plot_on_surface():

    sample = HandwritingSample.from_svc(svc_file)
    sample.visualizer.plot_on_surface_movement(sample)
    print(sample)

    assert sample


def test_plot_in_air():

    sample = HandwritingSample.from_svc(svc_file)
    sample.visualizer.plot_in_air_movement(sample)
    print(sample)

    assert sample


def test_plot_separate_movements():

    sample = HandwritingSample.from_svc(svc_file)
    sample.visualizer.plot_separate_movements(sample)
    print(sample)

    assert sample


def test_plot_strokes():

    sample = HandwritingSample.from_svc(svc_file)
    sample.visualizer.plot_strokes(sample)
    print(sample)

    assert sample


def test_plot_x():
    sample = HandwritingSample.from_svc(svc_file)
    sample.visualizer.plot_line(sample.x, x_label='sample', y_label='x [mm]')

    assert sample


def test_plot_y():
    sample = HandwritingSample.from_svc(svc_file)
    sample.visualizer.plot_line(sample.y, x_label='sample', y_label='y [mm]')

    assert sample


def test_plot_time():
    sample = HandwritingSample.from_svc(svc_file)
    sample.visualizer.plot_line(sample.time, x_label='sample', y_label='time [s]')

    assert sample


def test_plot_azimuth():
    sample = HandwritingSample.from_svc(svc_file)
    sample.visualizer.plot_line(sample.azimuth, x_label='sample', y_label='azimuth [°]')

    assert sample


def test_plot_tilt():
    sample = HandwritingSample.from_svc(svc_file)
    sample.visualizer.plot_line(sample.tilt, x_label='sample', y_label='tilt [°]')

    assert sample


def test_plot_all_data():
    sample = HandwritingSample.from_svc(svc_file)
    sample.visualizer.plot_all_modalities(sample)

    assert sample

