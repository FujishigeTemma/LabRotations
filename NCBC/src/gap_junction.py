import os

import click
import matplotlib.pyplot as plt
from neuron import h
from neuron.units import ms, mV

from cells import BasketCell


@click.command()
@click.option("-o", "--output", default="outputs", type=click.Path(exists=True), help="Path to output directory.")
def simulate_gap_junction(output: str) -> None:
    pv1 = BasketCell(0)
    pv2 = BasketCell(1)

    gap1 = h.gap(pv1.soma(0.5))
    gap2 = h.gap(pv2.soma(0.5))

    gap1.r = 2e2
    gap1.delay = 5
    gap2.r = 2e2
    gap2.delay = 5

    h.setpointer(pv2.soma(0.5)._ref_v, "v_pair", gap1)
    h.setpointer(pv1.soma(0.5)._ref_v, "v_pair", gap2)

    stimulus = h.IClamp(pv1.dendrites[0](1))

    stimulus.delay = 100 * ms
    stimulus.dur = 200 * ms
    stimulus.amp = 0.02  # nA

    pv1_v = h.Vector().record(pv1.soma(0.5)._ref_v)
    pv2_v = h.Vector().record(pv2.soma(0.5)._ref_v)
    t = h.Vector().record(h._ref_t)

    h.finitialize(-65 * mV)
    h.continuerun(400 * ms)

    fig, ax = plt.subplots()

    ax.plot(t, pv1_v, label="pv1")
    ax.plot(t, pv2_v, label="pv2")
    ax.set(xlabel="t (ms)", ylabel="v (mV)")
    ax.legend()

    ax.set_ylim(bottom=-60.5)

    plt.savefig(os.path.join(output, "gap_junction.png"))
