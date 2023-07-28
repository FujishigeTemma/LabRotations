import os

import click
import numpy as np
from scipy import stats  # type: ignore

import simulator
from networks import DentateGyrus
from recorders import VoltageRecorder
from spikes import inhomogeneous_poisson_process


@click.command()
@click.option("-o", "--output", default="outputs", type=click.Path(exists=True), help="Path to output directory.")
def simulate_dentate_gyrus(output: str):
    simulator.setup(seed=1)
    
    DG = DentateGyrus()

    n_connection_patterns = 24
    
    temporal_patterns = [inhomogeneous_poisson_process(t_start=0, t_stop=0.5, sampling_interval=0.001, rate_profile_frequency=10, rate_profile_amplitude=110) for _ in range(n_connection_patterns)]

    n_cells = len(DG.GCs.cells)
    pdf = stats.norm.pdf(np.arange(n_cells), loc=n_cells/2, scale=n_cells/2)
    pdf /= pdf.sum() # type: ignore

    indeces = np.arange(n_cells)
    centers = np.random.randint(0, n_cells, size=n_connection_patterns)

    for i, center in enumerate(centers):
        relative = np.roll(indeces, -center)
        spatial_pattern = np.random.choice(relative, size=100, p=pdf, replace=False)
        DG.evoke_GC(temporal_patterns[i].tolist(), spatial_pattern.tolist(), weight=0.001)

    n_cells = len(DG.BCs.cells)
    pdf = stats.norm.pdf(np.arange(n_cells), loc=n_cells/2, scale=n_cells/2)
    pdf /= pdf.sum() # type: ignore

    indeces = np.arange(n_cells)
    # centers = np.random.randint(0, n_cells, size=n_connection_patterns)
    centers = (centers / len(DG.GCs.cells) * len(DG.BCs.cells)).astype(int)

    for i, center in enumerate(centers):
        relative = np.roll(indeces, -center)
        spatial_pattern = np.random.choice(relative, size=1, p=pdf, replace=False)
        DG.evoke_BC(temporal_patterns[i].tolist(), spatial_pattern.tolist(), weight=0.001)

    vr = VoltageRecorder(DG)
    simulator.run(warmup=2000, duration=600)
    fig = vr.plot()

    fig.savefig(os.path.join(output, "dentate_gyrus.png"))