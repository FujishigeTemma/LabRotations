import h5py as h5
import matplotlib.pyplot as plt
import numpy as np
from neuron import h

from cells import Cell
from networks import Network


class VoltageRecorder:
    def __init__(self, network: Network):
        self.records_by_population_id = {}

        self.t = h.Vector()
        self.t.record(h._ref_t)

        for population in network.populations:
            records = []
            for cell in population.cells:
                records.append(recordVoltage(cell))
            self.records_by_population_id[population.id] = records

    def save(self, path: str):
        with h5.File(path, "a") as f:
            for population_id, records in self.records_by_population_id.items():
                dataset = f.require_dataset(
                    f"voltages/{population_id}",
                    shape=(len(records),),
                    dtype=h5.vlen_dtype(np.float64),
                )
                dataset[:] = [record.as_numpy() for record in records]

    def plot(self):
        nrow = len(self.records_by_population_id)
        fig, axes = plt.subplots(nrows=nrow, ncols=1, figsize=(8.27, 11.69))

        if nrow == 1:
            axes = np.array([axes])

        for i, population_id in enumerate(self.records_by_population_id.keys()):
            records = self.records_by_population_id[population_id]

            axes[i].plot(self.t, records[0].as_numpy())
            axes[i].set_ylabel(population_id)
            axes[i].set_xlim(0, 600)

        axes[-1].set_xlabel("Time (ms)")

        return fig


def recordVoltage(cell: Cell):
    v = h.Vector()
    v.record(cell.soma(0.5)._ref_v)
    return v
