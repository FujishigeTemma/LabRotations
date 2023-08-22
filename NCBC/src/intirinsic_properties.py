import os

import click
import matplotlib.pyplot as plt
import numpy as np
from neuron import h

from cells import BasketCell, Cell, GranuleCell, HippCell, MossyCell
from simulator import simulator


def current_clamp(cell: Cell, amplitude: float, duration: float, delay: float):
    stim = h.IClamp(cell.soma(0.5))
    stim.amp = amplitude
    stim.dur = duration
    stim.delay = delay
    return stim


def voltage_recording(cell: Cell):
    v = h.Vector()
    v.record(cell.soma(0.5)._ref_v)
    return v


@click.command()
@click.option("-o", "--output", default="outputs", type=click.Path(exists=True), help="Path to output directory.")
def analyze_intrinsic_properties(output: str):
    amplitudes = np.arange(0, 0.6, 0.025)

    cells: list[Cell] = [GranuleCell(0), MossyCell(0), BasketCell(0), HippCell(0)]
    cell_voltages = {cell.name: [] for cell in cells}
    cell_ap_counts = {cell.name: [] for cell in cells}

    for amp in amplitudes:
        simulator.setup(seed=0)

        t = h.Vector()
        t.record(h._ref_t)

        stims = []
        vs = []
        aps = []
        for cell in cells:
            stim = current_clamp(cell, amp, 500, 50)
            v = voltage_recording(cell)
            ap = h.APCount(cell.soma(0.5))

            stims.append(stim)
            vs.append(v)
            aps.append(ap)

        simulator.run(warmup=2000, duration=700)

        for cell, v, ap in zip(cells, vs, aps):
            cell_voltages[cell.name].append(np.array(v))
            cell_ap_counts[cell.name].append(ap.n / 0.5)

    fig, axes = plt.subplots(nrows=len(cells), ncols=1, figsize=(8.27, 11.69))

    for ax, cell in zip(axes, cells):
        ax.plot(amplitudes * 1000, cell_ap_counts[cell.name], marker="o")
        ax.set_title(f"{cell.name} F-I Curve")
        ax.set_xlabel("Current Injection (pA)")
        ax.set_ylabel("Frequency (Hz)")

    fig.tight_layout()
    fig.savefig(os.path.join(output, "intrinsic_properties.png"))
