import os

import click
import matplotlib.pyplot as plt
import numpy as np
from neuron import h
from neuron.units import ms, mV
from scipy import signal  # type: ignore

from cells import BasketCell, GranuleCell

h.load_file("stdrun.hoc")


@click.command()
@click.option("-o", "--output", default="outputs", type=click.Path(exists=True), help="Path to output directory.")
@click.option("--negative", is_flag=True, help="Use negative current.")
def simulate_gap_junction(output: str, negative: bool) -> None:
    pv1 = BasketCell(0)
    pv2 = BasketCell(1)

    # 150 µm
    # see https://www.nature.com/articles/s41467-018-06899-3/figures/4
    gap1 = h.gap(pv1.dendrites[1](0.5))
    gap2 = h.gap(pv2.dendrites[1](0.5))

    gap1.r = 6e2
    gap1.delay = 5
    gap2.r = 6e2
    gap2.delay = 5

    h.setpointer(pv2.dendrites[1](0.5)._ref_v, "v_pair", gap1)
    h.setpointer(pv1.dendrites[1](0.5)._ref_v, "v_pair", gap2)

    # supress spikes
    if not negative:
        normalize_stimulus_1 = h.IClamp(pv1.dendrites[0](1))
        normalize_stimulus_1.delay = 100 * ms
        normalize_stimulus_1.dur = 400 * ms
        normalize_stimulus_1.amp = -0.15  # nA

        normalize_stimulus_2 = h.IClamp(pv2.dendrites[0](1))
        normalize_stimulus_2.delay = 100 * ms
        normalize_stimulus_2.dur = 400 * ms
        normalize_stimulus_2.amp = -0.15  # nA

    # prepare stimulus
    stimulus = h.IClamp(pv1.dendrites[0](1))

    stimulus.delay = (300 if not negative else 100) * ms
    stimulus.dur = 200 * ms
    stimulus.amp = 0.2 if not negative else -0.2  # nA

    # record
    pv1_v = h.Vector().record(pv1.soma(0.5)._ref_v)
    pv2_v = h.Vector().record(pv2.soma(0.5)._ref_v)
    t = h.Vector().record(h._ref_t)

    # run
    h.finitialize(-69.9 * mV)
    h.continuerun((600 if not negative else 400) * ms)

    # prepare figure
    fig, ax = plt.subplots()

    ax.plot(t, pv1_v, label="pv1")
    ax.plot(t, pv2_v, label="pv2")
    ax.set(xlabel="t (ms)", ylabel="v (mV)")
    ax.legend()

    # calculate coupling coefficient
    baseline = pv1_v[(200 if not negative else 80) * 40]

    sample_time = (400 if not negative else 200) * 40
    pv1_v_max = pv1_v[sample_time] - baseline
    pv2_v_max = pv2_v[sample_time] - baseline

    ax.vlines(
        t[sample_time],
        ymin=pv1_v[sample_time],
        ymax=pv1_v[sample_time] + 1,
        color="red",
        label="peaks",
    )
    ax.vlines(
        t[sample_time],
        ymin=pv2_v[sample_time],
        ymax=pv2_v[sample_time] + 1,
        color="red",
    )

    coefficient = pv2_v_max / pv1_v_max

    print(f"Coupling coefficient: {coefficient:.3f}")
    ax.set_title(f"Coupling coefficient: {coefficient:.3f}")

    plt.savefig(os.path.join(output, "gap_junction.png" if not negative else "gap_junction_negative.png"))


@click.command()
@click.option("-o", "--output", default="outputs", type=click.Path(exists=True), help="Path to output directory.")
def simulate_EPSP_propagation(output: str):
    gc = GranuleCell(0)

    pv1 = BasketCell(0)
    pv2 = BasketCell(1)

    # prepare gap junctions
    gap1 = h.gap(pv1.dendrites[1](0.5))
    gap2 = h.gap(pv2.dendrites[1](0.5))

    gap1.r = 6e2
    gap1.delay = 5
    gap2.r = 6e2
    gap2.delay = 5

    h.setpointer(pv2.dendrites[1](0.5)._ref_v, "v_pair", gap1)
    h.setpointer(pv1.dendrites[1](0.5)._ref_v, "v_pair", gap2)

    # suppress spikes
    normalize_stimulus_1 = h.IClamp(pv1.dendrites[0](1))
    normalize_stimulus_1.delay = 100 * ms
    normalize_stimulus_1.dur = 300 * ms
    normalize_stimulus_1.amp = -0.15  # nA

    normalize_stimulus_2 = h.IClamp(pv2.dendrites[0](1))
    normalize_stimulus_2.delay = 100 * ms
    normalize_stimulus_2.dur = 300 * ms
    normalize_stimulus_2.amp = -0.15  # nA

    # prepare synapse
    synapse = h.tmgsyn(pv1.get_sections_by_name("proxd")[0](0.5))
    synapse.tau_1 = 7.6
    synapse.tau_facilition = 500
    synapse.tau_recovery = 0
    synapse.U = 0.1
    synapse.e = 0

    netcon = h.NetCon(gc.soma(0.5)._ref_v, synapse, sec=gc.soma)
    netcon.threshold = 10
    netcon.delay = 0.8
    netcon.weight[0] = 2e-2

    # prepare stimulus
    stimulus = h.IClamp(gc.dendrites[0](1))

    stimulus.delay = 200 * ms
    stimulus.dur = 100 * ms
    stimulus.amp = 0.2  # nA

    # record
    gc_v = h.Vector().record(gc.soma(0.5)._ref_v)
    pv1_v = h.Vector().record(pv1.soma(0.5)._ref_v)
    pv2_v = h.Vector().record(pv2.soma(0.5)._ref_v)
    t = h.Vector().record(h._ref_t)

    # run
    h.finitialize(-69.9 * mV)
    h.continuerun(500 * ms)

    # prepare figure
    fig, axes = plt.subplots(nrows=2, ncols=1)

    axes[0].plot(t, gc_v, label="gc")

    axes[1].plot(t, pv1_v, label="pv1")
    axes[1].plot(t, pv2_v, label="pv2")

    # calculate coupling coefficient
    t = np.array(t)
    pv1_v = np.array(pv1_v, dtype=np.float64)
    pv2_v = np.array(pv2_v, dtype=np.float64)

    pv1_v_lmax = signal.argrelmax(pv1_v)[0][1:-1]
    pv2_v_lmax = signal.argrelmax(pv2_v)[0][1:-1]

    axes[1].vlines(
        t[pv1_v_lmax],
        ymin=pv1_v[pv1_v_lmax],
        ymax=pv1_v[pv1_v_lmax] + 1,
        color="red",
        label="peaks",
    )
    axes[1].vlines(t[pv2_v_lmax], ymin=pv2_v[pv2_v_lmax], ymax=pv2_v[pv2_v_lmax] + 1, color="red")

    baseline = pv1_v[200 * 40]

    pv1_v_lmax = pv1_v[pv1_v_lmax] - baseline
    pv2_v_lmax = pv2_v[pv2_v_lmax] - baseline

    coefficient = np.mean(pv2_v_lmax / pv1_v_lmax)

    print(f"Coupling coefficient: {coefficient:.3f}")
    axes[1].set_title(f"Coupling coefficient: {coefficient:.3f}")

    for ax in axes:
        ax.set(xlabel="t (ms)", ylabel="v (mV)")
        ax.legend()

    fig.tight_layout()

    plt.savefig(os.path.join(output, "EPSP_propagation.png"))
