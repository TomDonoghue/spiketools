"""Functions to compute trial-related measures."""

import numpy as np

from spiketools.utils.select import get_avg_func
from spiketools.utils.checks import check_time_bins
from spiketools.measures.measures import compute_firing_rate
from spiketools.measures.conversions import convert_times_to_rates

###################################################################################################
###################################################################################################

def compute_trial_frs(trial_spikes, bins, trange=None, smooth=None):
    """Compute continuous binned firing rates for a set of epoched spike times.

    Parameters
    ----------
    trial_spikes : list of 1d array
        Spike times per trial.
    bins : float or 1d array
        The binning to apply to the spiking data.
        If float, the length of each bin.
        If array, precomputed bin definitions.
    trange : list of [float, float]
        Time range, in seconds, to create the binned firing rate across.
        Only used if `bins` is a float.
    smooth : float, optional
        If provided, the kernel to use to smooth the continuous firing rate.

    Returns
    -------
    trial_cfrs : 2d array
        Continuous firing rates per trial, with shape [n_trials, n_time_bins].
    """

    bins = check_time_bins(bins, trial_spikes[0], trange=trange)
    trial_cfrs = np.zeros([len(trial_spikes), len(bins) - 1])
    for ind, t_spikes in enumerate(trial_spikes):
        trial_cfrs[ind, :] = convert_times_to_rates(t_spikes, bins, smooth)

    return trial_cfrs


def compute_pre_post_rates(trial_spikes, pre_window, post_window):
    """Compute the firing rates in pre and post event windows.

    Parameters
    ----------
    trial_spikes : list of 1d array
        Spike times per trial.
    pre_window, post_window : list of [float, float]
        The time window to compute firing rate across, for the pre and post event windows.

    Returns
    -------
    frs_pre, frs_post : 1d array
        Computed pre & post firing rate for each trial.
    """

    frs_pre = np.array([compute_firing_rate(trial, *pre_window) for trial in trial_spikes])
    frs_post = np.array([compute_firing_rate(trial, *post_window) for trial in trial_spikes])

    return frs_pre, frs_post


def compute_pre_post_averages(frs_pre, frs_post, avg_type='mean'):
    """Compute the average firing rate across pre & post event windows.

    Parameters
    ----------
    frs_pre, frs_post : 1d array
        Firing rates across pre & post event windows.
    avg_type : {'mean', 'median'}
        The type of averaging function to use.

    Returns
    -------
    avg_pre, avg_post : float
        The average firing rates for the pre & post event windows.
    """

    avg_pre = get_avg_func(avg_type)(frs_pre)
    avg_post = get_avg_func(avg_type)(frs_post)

    return avg_pre, avg_post
