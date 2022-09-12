"""Utility functions for extracting data segments of interest."""

import numpy as np

from spiketools.utils.options import get_comp_func

###################################################################################################
###################################################################################################

def create_mask(data, min_value=None, max_value=None):
    """Create a mask to select data points based on value.

    Parameters
    ----------
    data : 1d array
        Array of data.
    min_value, max_value : float, optional
        Minimum and/or maximum value to extract from the input array.
    reset : float, optional
        If provided, resets the values in the data array by the given reset value.

    Returns
    -------
    mask : 1d array of bool
        Mask to select data points from the input array.

    Examples
    --------
    Create a mask to select data within a given value range:

    >>> data = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    >>> create_mask(data, min_value=3, max_value=6)
    array([False, False,  True,  True,  True,  True, False, False])
    """

    min_value = -np.inf if min_value is None else min_value
    max_value = np.inf if max_value is None else max_value

    mask = np.logical_and(data >= min_value, data <= max_value)

    return mask


def get_range(data, min_value=None, max_value=None, reset=None):
    """Get a specified range from a vector of data.

    Parameters
    ----------
    data : 1d array
        Array of data.
    min_value, max_value : float, optional
        Minimum and/or maximum value to extract from the input array.
    reset : float, optional
        If provided, resets the values in the data array by the given reset value.

    Returns
    -------
    data : 1d array
        Data array, restricted to desired time range.

    Examples
    --------
    Get all values greater than a specific value:

    >>> data = np.array([5, 10, 15, 20, 25, 30])
    >>> get_range(data, min_value=10, max_value=None)
    array([10, 15, 20, 25, 30])

    Get all values less than a specific value:

    >>> data = np.array([5, 10, 15, 20, 25, 30])
    >>> get_range(data, min_value=None, max_value=25)
    array([ 5, 10, 15, 20, 25])

    Get a specified range from a data array:

    >>> data = np.array([5, 10, 15, 20, 25, 30])
    >>> get_range(data, min_value=10, max_value=20)
    array([10, 15, 20])
    """

    mask = create_mask(data, min_value, max_value)

    data = data[mask]

    if reset:
        data = data - reset

    return data


def get_value_range(times, data, min_value=None, max_value=None, reset=None):
    """Extract data and associated timestamps for a desired value range.

    Parameters
    ----------
    times : 1d array
        Time indices.
    data : 1d array
        Array of data.
    min_value, max_value : float, optional
        Minimum and/or maximum value to extract from the input array.
    reset : float, optional
        If provided, resets the time values by the given reset value.

    Returns
    -------
    times : 1d array
        Time indices, selected by value.
    data : 1d array
        Array of data, selected by value.

    Examples
    --------
    Extract data and corresponding timestamps based on value range:

    >>> data = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    >>> times = np.array([0.2, 0.3, 0.4, 0.5, 0.7, 0.9, 1.2, 1.5])
    >>> get_value_range(times, data, min_value=3, max_value=6)
    (array([0.4, 0.5, 0.7, 0.9]), array([3, 4, 5, 6]))
    """

    mask = create_mask(data, min_value, max_value)

    times, data = times[mask], data[mask]

    if reset:
        times = times - reset

    return times, data


def get_ind_by_time(times, timepoint, threshold=None):
    """Get the index for a data array for a specified timepoint.

    Parameters
    ----------
    times : 1d array
        Time indices.
    timepoint : float
        Time value to extract the index for.
    threshold : float, optional
        The threshold that the closest time value must be within to be returned.
        If the temporal distance is greater than the threshold, output is -1.

    Returns
    -------
    ind : int
        The index value for the requested timepoint, or -1 if out of threshold range.

    Examples
    --------
    Get the index for a specified timepoint:

    >>> times = np.array([0.5, 1, 1.5, 2, 2.5, 3 ])
    >>> get_ind_by_time(times, 2.5)
    4
    """

    ind = np.abs(times - timepoint).argmin()
    if threshold:
        if np.abs(times[ind] - timepoint) > threshold:
            ind = -1

    return ind


def get_inds_by_times(times, timepoints, threshold=None, drop_null=True):
    """Get indices for a data array for a set of specified time points.

    Parameters
    ----------
    times : 1d array
        Time indices.
    timepoints : 1d array
        The time values to extract indices for.
    threshold : float, optional
        The threshold that the closest time value must be within to be returned.
        If the temporal distance is greater than the threshold, output is NaN.
    drop_null : bool, optional, default: True
        Whether to drop any null indices from the outputs (outside threshold range).
        If False, indices for any null values are -1.

    Returns
    -------
    inds : 1d array
        Indices for all requested timepoints.

    Examples
    --------
    Get the corresponding indices for specified timepoints:

    >>> times = np.array([0.5, 1, 1.5, 2, 2.5, 3 ])
    >>> timepoints = np.array([1, 2, 3])
    >>> get_inds_by_times(times, timepoints)
    array([1, 3, 5])
    """

    inds = np.zeros(len(timepoints), dtype=int)
    for ind, timepoint in enumerate(timepoints):
        inds[ind] = get_ind_by_time(times, timepoint, threshold=threshold)

    if drop_null:
        inds = inds[inds >= 0]

    return inds


def get_value_by_time(times, values, timepoint, threshold=None):
    """Get the value from a data array at a specific time point.

    Parameters
    ----------
    times : 1d array
        Time indices.
    values : 1d or 2d array
        Data values, corresponding to the times vector.
    timepoint : float
        Time value to extract.
    threshold : float, optional
        The threshold that the closest time value must be within to be returned.
        If the temporal distance is greater than the threshold, output is NaN.

    Returns
    -------
    out : float or 1d array
        The value(s) at the requested time point.

    Examples
    --------
    Get the data values for a specified timepoint:

    >>> times = np.array([0.5, 1, 1.5, 2, 2.5, 3 ])
    >>> values = np.array([[1,2,3,4,5,6], [7,8,9,10,11,12]])
    >>> get_value_by_time(times, values, 1.5)
    array([3, 9])
    """

    idx = get_ind_by_time(times, timepoint, threshold=threshold)
    out = values.take(indices=idx, axis=-1) if idx >= 0 else np.nan

    return out


def get_values_by_times(times, values, timepoints, threshold=None, drop_null=True):
    """Get values from a data array for a set of specified time points.

    Parameters
    ----------
    times : 1d array
        Time indices.
    values : 1d or 2d array
        Data values, corresponding to the times vector.
    timepoints : 1d array
        The time indices to extract corresponding values for.
    threshold : float, optional
        The threshold that the closest time value must be within to be returned.
        If the temporal distance is greater than the threshold, output is NaN.
    drop_null : bool, optional, default: True
        Whether to drop any null values from the outputs (outside threshold range).
        If False, indices for any null values are NaN.

    Returns
    -------
    outputs : 1d or 2d array
        The extracted values for the requested time points.

    Examples
    --------
    Get the data values for a specified set of timepoints:

    >>> times = np.array([0.5, 1, 1.5, 2, 2.5, 3 ])
    >>> values = np.array([1, 2, 3, 4, 5, 6])
    >>> timepoints = np.array([1, 2, 3])
    >>> get_values_by_times(times, values, timepoints)
    array([2, 4, 6])
    """

    inds = get_inds_by_times(times, timepoints, threshold, drop_null)

    if drop_null:
        outputs = values.take(indices=inds, axis=-1)
    else:
        outputs = np.full([np.atleast_2d(values).shape[0], len(timepoints)], np.nan)
        mask = inds >= 0
        outputs[:, np.where(mask)[0]] = values.take(indices=inds[mask], axis=-1)
        outputs = np.squeeze(outputs)

    return outputs


def get_values_by_time_range(times, values, t_min, t_max):
    """Extract data for a requested time range.

    Parameters
    ----------
    times : 1d array
        Time indices.
    values : ndarray
        Data values, corresponding to the times indices.
    t_min, t_max : float
        Time range to extract.

    Returns
    -------
    times : 1d array
        Selected time indices.
    out : ndarray
        Selected values.

    Examples
    --------
    Extract data within a specified time range:

    >>> times = np.array([1, 2, 3, 4, 5, 6, 7])
    >>> values = np.array([0.5, 1, 1.5, 2, 2.5, 3, 3.5])
    >>> get_values_by_time_range(times, values, t_min=2, t_max=6)
    (array([2, 3, 4, 5, 6]), array([1. , 1.5, 2. , 2.5, 3. ]))
    """

    select = np.logical_and(times >= t_min, times <= t_max)
    out = values.take(indices=np.where(select)[0], axis=-1)

    return times[select], out


def threshold_spikes_by_times(spikes, times, threshold):
    """Threshold spikes by sub-selecting those are temporally close to a set of time values.

    Parameters
    ----------
    spikes : 1d array
        Spike times, in seconds.
    times : 1d array
        Time indices.
    threshold : float
        The threshold that closest time values must be within to be kept.
        For any time indices greater than this threshold, the spike value is dropped.

    Returns
    -------
    spikes : 1d array
        Sub-selected spike times, in seconds.
    """

    mask = np.empty_like(spikes, dtype=bool)
    for ind, spike in enumerate(spikes):
        mask[ind] = np.min(np.abs(times - spike)) < threshold

    return spikes[mask]


def threshold_spikes_by_values(spikes, times, values, data_threshold,
                               time_threshold=None, comp_type='greater'):
    """Threshold spikes by sub-selecting those are exceed a value on another data stream.

    Parameters
    ----------
    spikes : 1d array
        Spike times, in seconds.
    times : 1d array
        Time indices.
    values : 1d array
        Data values, corresponding to the times vector.
    data_threshold : float
        The threshold that closest data values must be within to be kept.
    time_threshold : float, optional
        The threshold that closest time values must be within to be kept.
        For any time indices greater than this threshold, the spike value is dropped.
    comp_type : {'greater', 'less'}
        Which comparison function to use.
        This defines whether selected values must be greater than or less than the data threshold.

    Returns
    -------
    spikes : 1d array
        Sub-selected spike times, in seconds.

    Examples
    --------
    Threshold spikes based on a a minimum data threshold:

    >>> spikes = np.array([0.1, 0.3, 0.4, 0.5, 1, 1.2, 1.6, 1.8])
    >>> times = np.array([0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4])
    >>> values = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    >>> threshold_spikes_by_values(spikes, times, values, 2)
    array([1.6, 1.8])
    """

    values = get_values_by_times(times, values, spikes, time_threshold, drop_null=False)

    mask = ~np.isnan(values)
    spikes, values = spikes[mask], values[mask]
    spikes = spikes[get_comp_func(comp_type)(values, data_threshold)]

    return spikes


def drop_range(spikes, time_range, check_empty=True):
    """Drop a specified time range from a vector spike times.

    Parameters
    ----------
    spikes : 1d array
        Spike times, in seconds.
    time_range : list of [float, float] or list of list of [float, float]
        Time range(s) to drop from spike times.
        Each time range should be defined as [start_add_time, end_add_time].
    check_empty : bool, optional, default: True
        Whether to check if the dropped range is empty of spikes.
        If True, and there are spikes within the drop `time_range`, an error is raised.

    Returns
    -------
    out_spikes : 1d array
        Spike times, in seconds, with the time range removed.
    """

    # Operate on a copy of the input, to not overwrite original array
    spikes = spikes.copy()

    total_len = 0
    for trange in np.array(time_range, ndmin=2):

        if total_len > 0:
            trange = [trange[0] - total_len, trange[1] - total_len]

        if check_empty:
            assert get_range(spikes, *trange).size == 0, \
                "Extracted range {} is not empty.".format(trange)

        tlen = trange[1] - trange[0]
        spikes = np.hstack([get_range(spikes, max_value=trange[0]),
                            get_range(spikes, min_value=trange[1], reset=tlen)])

        total_len += trange[1] - trange[0]

    return spikes


def _reinstate_range_1d(spikes, time_range):
    """Reinstate a dropped time range into a vector of spike times.

    Parameters
    ----------
    spikes : 1d array
        Spike times, in seconds.
    time_range : list of [float, float]
        Time range to reinstate into spike times, as [start_add_time, end_add_time].

    Returns
    -------
    out_spikes : 1d array
        Spike times, in seconds, with the time range reinstated.
    """

    tlen = time_range[1] - time_range[0]
    out_spikes = np.hstack([get_range(spikes, max_value=time_range[0]),
                            get_range(spikes, min_value=time_range[0]) + tlen])

    return out_spikes


def reinstate_range(spikes, time_range):
    """Reinstate a dropped time range into an array of spike times.

    Parameters
    ----------
    spikes : 1d or 2d array
        An array of spikes times, in seconds.
    time_range : list of [float, float] or list of list of [float, float]
        Time range(s) to reinstate into shuffled spike times.
        Each time range should be defined as [start_add_time, end_add_time].

    Returns
    -------
    spikes_out : 1d or 2d array
        An array of spikes times, in seconds, with the time range reinstated.
    """

    assert spikes.ndim < 3, 'The reinstate_range function only supports 1d or 2d arrays.'

    # Operate on a copy of the input, to not overwrite original array
    spikes = spikes.copy()

    # By enforcing 2d (and later squeezing), the loops works for both 1d & 2d arrays
    spikes = np.atleast_2d(spikes)
    for trange in np.array(time_range, ndmin=2):
        for ind, spikes_1d in enumerate(spikes):
            spikes[ind, :] = _reinstate_range_1d(spikes_1d, trange)

    spikes = np.squeeze(spikes)

    return spikes
