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

