import matplotlib.pyplot as plt
from neuron import h

from cells import Cell
from networks import Network


class ActionPotentialRecorder:
    records_by_population_id: dict[str, list]
    counters_by_population_id: dict[str, list]

    def __init__(self, network: Network):
        self.records_by_population_id = {}
        self.counters_by_population_id = {}
        for population in network.populations:
            records = []
            counters = []
            for cell in population.cells:
                record, counter = recordAP(cell, threshold=0)
                records.append(record)
                counters.append(counter)
            self.records_by_population_id[population.id] = records
            self.counters_by_population_id[population.id] = counters

    def plot(self):
        fig, axes = plt.subplots(nrows=len(self.records_by_population_id), ncols=1, figsize=(8.27, 11.69))

        for i, population_id in enumerate(self.records_by_population_id.keys()):
            records = self.records_by_population_id[population_id]

            axes[i].eventplot([record.as_numpy() for record in records])
            axes[i].set_ylabel(f"{population_id}\n{calc_active_cell_percentage(records):.2f}% Active")
            axes[i].set_xlim(0, 600)
        
        axes[-1].set_xlabel("Time (ms)")
        
        return fig

def recordAP(cell: Cell, threshold: float):
    counter = h.APCount(cell.soma(0.5))
    counter.thresh = threshold

    record = h.Vector()
    counter.record(record)
    
    return record, counter

def calc_active_cell_percentage(records: list):
        n_active_cells = 0
        for record in records:
            if len(record) > 0:
                n_active_cells += 1
        
        return n_active_cells / len(records) * 100
