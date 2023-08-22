import numpy as np
from numpy.typing import NDArray
from scipy.interpolate import interp1d


def inhomogeneous_poisson_process(
    t_start: float, t_stop: float, sampling_interval: float, rate_profile_frequency: int, rate_profile_amplitude: int, refractory_period: float | None = None
) -> NDArray[np.float64]:
    """
    Generates a spike train from an inhomogeneous Poisson process.
    NOTE: units are seconds.
    """

    t = np.arange(t_start, t_stop, sampling_interval)

    rate_profile = rate_profile_amplitude * (np.sin(t * rate_profile_frequency * np.pi * 2 - np.pi / 2) + 1) / 2

    cumulative_rate = np.cumsum(rate_profile) * sampling_interval
    max_cumulative_rate = cumulative_rate[-1]
    n_spikes = np.round(max_cumulative_rate).astype(int)

    random_numbers = np.random.uniform(0, max_cumulative_rate, n_spikes)

    inv_cumulative_rate_func = interp1d(cumulative_rate, t)

    spike_times: NDArray[np.float64] = inv_cumulative_rate_func(random_numbers)
    spike_times.sort()

    if refractory_period is None:
        return spike_times

    thinned_spike_times = np.empty(0, dtype=np.float64)
    previous_spike_time = t_start - refractory_period

    for spike_time in spike_times:
        if spike_time - previous_spike_time > refractory_period:
            thinned_spike_times = np.append(thinned_spike_times, spike_time)
            previous_spike_time = spike_time

    return thinned_spike_times
