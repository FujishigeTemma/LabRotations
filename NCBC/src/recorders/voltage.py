import matplotlib.pyplot as plt
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

    def plot(self):
        fig, axes = plt.subplots(nrows=len(self.records_by_population_id), ncols=1, figsize=(8.27, 11.69))

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