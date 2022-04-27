"""Utilities for managing trials and epochs."""

from spiketools.utils.data import restrict_range, get_value_by_time_range

###################################################################################################
###################################################################################################

def epoch_spikes_by_event(spikes, events, window):
    """Epoch spiking data into trials, based on events of interest.

    Parameters
    ----------
    spikes : 1d array
        Spike times.
    events : 1d array
        The set of event times to extract from the data.
    window : list of [float, float]
        The time window to extract around each event.

    Returns
    -------
    trials : list of 1d array
        Spike data per trial.

    Notes
    -----
    For each trial, the returned spike times will be relative to each event time, set as zero.
    """

    trials = [None] * len(events)
    for ind, event in enumerate(events):
        trials[ind] = restrict_range(spikes, event + window[0], event + window[1]) - event

    return trials


def epoch_spikes_by_range(spikes, starts, stops, reset=False):
    """Epoch spiking data into trials, based on time ranges of interest.

    Parameters
    ----------
    spikes : 1d array
        Spike times.
    starts : list
        The start times for each epoch to extract.
    stops : list
        The stop times of each epoch to extract.
    reset : bool, optional, default: False
        Whether to reset each set of trial timestamps to start at zero.

    Returns
    -------
    trials : list of 1d array
        Spike data per trial.
    """

    trials = [None] * len(starts)
    for ind, (start, stop) in enumerate(zip(starts, stops)):
        trial = restrict_range(spikes, start, stop)
        if reset:
            trial = trial - start
        trials[ind] = trial

    return trials


def epoch_data_by_event(timestamps, values, events, window):
    """Epoch data with timestamps into trials, based on events of interest.

    Parameters
    ----------
    timestamps : 1d array
        Timestamps.
    values : 1d array
        Data values.
    events : 1d array
        The set of event times to extract from the data.
    window : list of [float, float]
        The time window to extract around each event.

    Returns
    -------
    trial_times : list of 1d array
        The timestamps, per trial.
    trial_values : list of 1d array
        The values, per trial.
    """

    trial_times = [None] * len(events)
    trial_values = [None] * len(events)
    for ind, event in enumerate(events):
        ttimes, tvalues = get_value_by_time_range(\
            timestamps, values, event + window[0], event + window[1])
        trial_times[ind] = ttimes - event
        trial_values[ind] = tvalues

    return trial_times, trial_values


def epoch_data_by_range(timestamps, values, starts, stops, reset=False):
    """Epoch data with timestamps into trials, based on time ranges of interest.

    Parameters
    ----------
    timestamps : 1d array
        Timestamps.
    values : 1d array
        Data values.
    starts : list
        The start times for each epoch to extract.
    stops : list
        The stop times of each epoch to extract.

    Returns
    -------
    trial_times : list of 1d array
        The timestamps, per trial.
    trial_values : list of 1d array
        The values, per trial.
    """

    trial_times = [None] * len(starts)
    trial_values = [None] * len(starts)
    for ind, (start, stop) in enumerate(zip(starts, stops)):
        ttimes, tvalues = get_value_by_time_range(timestamps, values, start, stop)
        if reset:
            ttimes = ttimes - start
        trial_times[ind] = ttimes
        trial_values[ind] = tvalues

    return trial_times, trial_values