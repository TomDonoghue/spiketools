"""Tests for spiketools.utils.checks"""

import numpy as np

from pytest import raises, warns

from spiketools.utils.checks import *

###################################################################################################
###################################################################################################

def test_check_param_range():

    # Check that valid options run without error
    check_param_range(0.5, 'test', [0., 1])
    check_param_range(0., 'test', [0., 1])
    check_param_range(1., 'test', [0., 1])
    check_param_range('a', 'test', ['a', 'b'])

    # Check that invalid options raise an error
    with raises(ValueError):
        check_param_range(-1, 'test', [0., 1])
    with raises(ValueError):
        check_param_range(1.5, 'test', [0., 1])

def test_check_param_options():

    # Check that valid options run without error
    check_param_options('a', 'test', ['a', 'b', 'c'])

    with raises(ValueError):
        check_param_options('a', 'test', ['b', 'c'])

def test_infer_time_unit(tspikes):

    # Check test data in seconds
    inferred = infer_time_unit(tspikes)
    assert inferred == 'seconds'

    # Check test data in milliseconds
    inferred = infer_time_unit(tspikes * 1000)
    assert inferred == 'milliseconds'

def test_check_bin_range():

    values = np.array([0.5, 1.5, 2.5, 3.5, 4.5])
    edges1 = np.array([0, 3, 6])
    edges2 = np.array([1, 2.5, 5])
    edges3 = np.array([0, 2, 4])

    check_bin_range(values, edges1)
    with warns(UserWarning):
        check_bin_range(values, edges2)
    with warns(UserWarning):
        check_bin_range(values, edges3)

def test_check_time_bins(tspikes):

    # Check precomputed time bins
    tbins = np.arange(0, 10 + 0.5, 0.5)
    out = check_time_bins(tbins, tspikes)
    assert np.array_equal(tbins, out)

    # Check time bins given a time resolution, which should create same bins as precomputed
    out = check_time_bins(0.5, tspikes, trange=[0, 10])
    assert np.array_equal(tbins, out)

    # Check error & warning
    with raises(AssertionError):
        out = check_time_bins(np.array([1, 2, 1]), tspikes, trange=[0, 5])
    with warns(UserWarning):
        out = check_time_bins(0.5, tspikes, trange=[0, 5])
