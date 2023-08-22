import numpy as np
from numpy.typing import NDArray


def homogeneous_poisson_process(t_start: float, t_stop: float, rate: float, refractory_period: float | None = None) -> NDArray[np.float64]:
    """
    Generates a spike train from a homogeneous Poisson process.
    NOTE: units are seconds.
    """

    n_spikes = np.random.poisson((t_stop - t_start) * rate)

    spike_times = np.random.uniform(t_start, t_stop, n_spikes)
    spike_times.sort()

    if refractory_period is None:
        return spike_times

    thinned_spike_times = np.empty(0)
    previous_spike_time = t_start - refractory_period

    for spike_time in spike_times:
        if spike_time - previous_spike_time > refractory_period:
            thinned_spike_times = np.append(thinned_spike_times, spike_time)
            previous_spike_time = spike_time

    return thinned_spike_times
