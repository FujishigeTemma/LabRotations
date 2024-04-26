import os

import click
import h5py as h5
import matplotlib.pyplot as plt
import numpy as np
import simulator
from networks import Ring
from numpy.fft import fft, fftfreq, fftshift
from recorders import DB, ActionPotentialRecorder, VoltageRecorder
from spikes import homogeneous_poisson_process, inhomogeneous_poisson_process
from typeid import TypeID, from_string


def set_job_id(ctx, param, value):
    if value is None:
        return TypeID(prefix="job")

    try:
        return from_string(value)
    except ValueError:
        raise click.BadParameter("must be a valid TypeID(prefix='job')")


@click.command()
@click.option("--job-id", type=click.UNPROCESSED, callback=set_job_id, help="ID of the job.")
@click.option("-s", "--seed", default=0, type=int, help="Random seed.")
@click.option(
    "--stimuli", default="inhomogeneous_poisson_process", type=click.Choice(["homogeneous_poisson_process", "inhomogeneous_poisson_process"]), help="Type of stimuli to evoke."
)
@click.option("-f", "--frequency", default=10, type=int, help="Frequency of the stimuli.")
@click.option("--n-cells", default=200, type=int, help="Number of cells in the ring.")
@click.option("--connectivity", default=0.3, type=float, help="Connectivity of the ring.")
@click.option("--with-gap-junctions", is_flag=True, help="Include gap junctions.")
@click.option("-o", "--output", default="outputs", type=click.Path(exists=True), help="Path to output directory.")
def simulate_ring(job_id: TypeID, seed: int, n_cells: int, connectivity: float, with_gap_junctions: bool, stimuli: str, frequency: int, output: str):
    return _simulate_ring(job_id, seed, n_cells, connectivity, with_gap_junctions, stimuli, frequency, output)


def _simulate_ring(job_id: TypeID, seed: int, n_cells: int, connectivity: float, with_gap_junctions: bool, stimuli: str, frequency: int, output: str):
    simulator.setup(seed=seed)

    RING = Ring(n_cells, connectivity, with_gap_junctions=with_gap_junctions)

    n_cells = len(RING.BCs.cells)

    temporal_patterns = []
    match stimuli:
        case "homogeneous_poisson_process":
            temporal_patterns = [
                (
                    homogeneous_poisson_process(
                        t_start=0,
                        t_stop=0.5,
                        rate=frequency,
                        refractory_period=0.001,
                    )
                    * 1000
                ).round(1)
                for _ in range(n_cells)
            ]
        case "inhomogeneous_poisson_process":
            temporal_patterns = [
                (
                    inhomogeneous_poisson_process(
                        t_start=0,
                        t_stop=0.5,
                        sampling_interval=0.0001,
                        rate_profile_frequency=frequency,
                        rate_profile_amplitude=100,
                        refractory_period=0.001,
                    )
                    * 1000
                ).round(1)
                for _ in range(n_cells)
            ]

    os.makedirs(os.path.join(output, str(job_id)), exist_ok=True)

    with h5.File(os.path.join(output, str(job_id), "ring.h5"), "a") as f:
        dataset = f.require_dataset(
            "action_potentials/input",
            shape=(len(temporal_patterns),),
            dtype=h5.vlen_dtype(np.float64),
        )
        dataset[:] = temporal_patterns

        dataset = f.require_dataset(
            "A",
            shape=RING.A.shape,
            dtype=RING.A.dtype,
        )
        dataset[:] = RING.A

    for i in range(n_cells):
        spatial_pattern = [i]
        RING.evoke_BC(temporal_patterns[i].tolist(), spatial_pattern, weight=0.01)

    vr = VoltageRecorder(RING)
    apr = ActionPotentialRecorder(RING)

    simulator.run(warmup=2000, duration=600)

    vr.save(os.path.join(output, str(job_id), "ring.h5"))
    apr.save(os.path.join(output, str(job_id), "ring.h5"))

    fig = vr.plot()
    fig.savefig(os.path.join(output, str(job_id), "voltages.png"))

    fig = apr.plot()
    fig.savefig(os.path.join(output, str(job_id), "action_potentials.png"))

    with DB(os.path.join(output, "ring.sqlite")) as db:
        row = {
            "id": str(job_id),
            "seed": seed,
            "n_cells": n_cells,
            "connectivity": connectivity,
            "with_gap_junctions": with_gap_junctions,
            "stimuli": stimuli,
            "frequency": frequency,
        }

        db.insert("jobs", row)

    plt.close("all")


@click.command()
@click.option("--job-id", required=True, type=click.UNPROCESSED, callback=set_job_id, help="ID of the job.")
@click.option("-o", "--output", default="outputs", type=click.Path(exists=True), help="Path to output directory.")
def analyze_ring(job_id: TypeID, output: str):
    with h5.File(os.path.join(output, str(job_id), "ring.h5"), "r") as f:
        APs = f["action_potentials"]
        assert isinstance(APs, h5.Group)

        fig1, axes1 = plt.subplots(ncols=1, nrows=2, figsize=(10, 5))
        for name, dataset in APs.items():
            fig2, axes2 = plt.subplots(ncols=1, nrows=2, figsize=(10, 5))

            spike_times = np.concatenate(dataset)

            axes2[0].eventplot(dataset)
            axes2[1].eventplot(spike_times)

            axes2[0].set_title(name)
            axes2[1].set_xlabel("Time (ms)")

            fig2.savefig(os.path.join(output, str(job_id), f"action_potential_{name}.png"))

            hist, bins = np.histogram(spike_times, bins=100)

            average_activity = np.mean(hist)

            axes1[0].plot(bins[:-1], hist, label=f"{name} Avg: {average_activity:.2f}")

            sampling_rate = len(bins) / (bins[-1] - bins[0]) * 1000

            sp = fftshift(fft(hist))
            freq = fftshift(fftfreq(len(hist), 1 / sampling_rate))

            amp = np.abs(sp)

            axes1[1].plot(freq[len(freq) // 2 :], amp[len(amp) // 2 :], label=name)

        axes1[0].set_xlabel("Time (ms)")
        axes1[0].set_ylabel("Spike Activity")
        axes1[0].set_xlim(0, 600)

        axes1[1].set_xlabel("Frequency (Hz)")
        axes1[1].set_ylabel("Amplitude")
        axes1[1].set_xlim(0, 200)
        axes1[1].set_ylim(0, 1000)

        axes1[0].legend(loc="upper right")
        axes1[1].legend(loc="upper right")

        fig1.tight_layout()
        fig1.savefig(os.path.join(output, str(job_id), "activity.png"))

    plt.close("all")
