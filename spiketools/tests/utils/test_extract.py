"""Tests for spiketools.utils.extract"""

import numpy as np

from spiketools.utils.extract import *

###################################################################################################
###################################################################################################

def test_restrict_range():

    data = np.array([0.5, 1., 1.5, 2., 2.5])

    out1 = restrict_range(data, min_value=1.)
    assert np.array_equal(out1, np.array([1., 1.5, 2., 2.5]))

    out2 = restrict_range(data, max_value=2.)
    assert np.array_equal(out2, np.array([0.5, 1., 1.5, 2.]))

    out3 = restrict_range(data, min_value=1., max_value=2.)
    assert np.array_equal(out3, np.array([1., 1.5, 2.]))

    out4 = restrict_range(data, min_value=1., max_value=2., reset=1.)
    assert np.array_equal(out4, np.array([0., 0.5, 1.0]))

def test_get_value_by_time():

    times = np.array([1, 2, 3, 4, 5])
    values = np.array([5, 8, 4, 6, 7])

    value_out = get_value_by_time(times, values, 3)
    assert value_out == values[2]

    value_out = get_value_by_time(times, values, 3.4)
    assert value_out == values[2]

def test_get_values_by_times():

    times = np.array([1, 2, 3, 4, 5])
    values = np.array([5, 8, 4, 6, 7])

    timepoints = np.array([1.75, 4.15])

    outputs = get_values_by_times(times, values, timepoints)
    assert len(outputs) == len(timepoints)
    assert np.array_equal(outputs, np.array([8, 6]))

def test_get_value_by_time_range():

    times = np.array([1, 2, 3, 4, 5])
    values = np.array([5, 8, 4, 6, 7])

    times_out, values_out = get_value_by_time_range(times, values, 2, 4)
    assert np.array_equal(times_out, np.array([2, 3, 4]))
    assert np.array_equal(values_out, np.array([8, 4, 6]))
