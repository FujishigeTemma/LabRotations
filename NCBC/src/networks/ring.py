from cells import BasketCell

from .network import Network
from .population import NetConParams, Population, TmgSynParams, connect, connect_gap, evoke


# Bartos et al. 2002
class Ring(Network):
    name = "Ring"

    def __init__(self, n_cells: int, connectivity: float, with_gap_junctions=False):
        self.BCs = Population(index=1, cell_type=BasketCell, n_cells=n_cells)

        self.populations = [self.BCs]

        # BC -> BC
        tmgsyn_params = TmgSynParams(tau_1=1.8, tau_facilition=0, tau_recovery=0, U=1, e=-70)
        netcon_params = NetConParams(threshold=10, delay=0.8, weight=7.6e-3)
        self.BC_TO_BC, self.A = connect(
            pre_population=self.BCs,
            post_population=self.BCs,
            n_candidates=int(n_cells * connectivity),
            n_synapses=int(n_cells * connectivity),
            target_section_name="proxd",
            tmgsyn_params=tmgsyn_params,
            netcon_params=netcon_params,
        )

        self.connections = [self.BC_TO_BC]

        if with_gap_junctions:
            self.BC_TO_BC_gap_junctions = connect_gap(self.BCs, self.BCs, 8, 4)

        self.BC_vecstims = []

    def evoke_BC(self, temporal_pattern: list[float], spatial_pattern: list[int], weight: float):
        tmgsyn_params = TmgSynParams(tau_1=6.3, tau_facilition=0, tau_recovery=0, U=1, e=0)
        netcon_params = NetConParams(threshold=10, delay=1, weight=weight)
        connections, vecstim = evoke(
            population=self.BCs,
            temporal_pattern=temporal_pattern,
            spatial_pattern=spatial_pattern,
            target_section_name="ddend",
            tmgsyn_params=tmgsyn_params,
            netcon_params=netcon_params,
        )

        self.BC_vecstims.append(vecstim)
        self.connections.append(connections)
