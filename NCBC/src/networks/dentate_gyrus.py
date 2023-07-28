from cells import BasketCell, GranuleCell, HippCell, MossyCell

from .network import Network
from .population import NetConParams, Population, TmgSynParams, connect, evoke


class DentateGyrus(Network):
    name = "Dentate Gyrus"

    def __init__(self):
        self.GCs = Population(index=1, cell_type=GranuleCell, n_cells=2000)
        self.MCs = Population(index=1, cell_type=MossyCell, n_cells=60)
        self.BCs = Population(index=1, cell_type=BasketCell, n_cells=24)
        self.HCs = Population(index=1, cell_type=HippCell, n_cells=24)

        self.populations = [self.GCs, self.MCs, self.BCs, self.HCs]

        # GC -> MC
        tmgsyn_params = TmgSynParams(tau_1=7.6, tau_facilition=500, tau_recovery=0, U=0.1, e=0)
        netcon_params = NetConParams(threshold=10, delay=1.5, weight=2e-2)
        self.GC_TO_MC = connect(pre_population=self.GCs, post_population=self.MCs, n_candidates=12, n_synapses=1, target_section_name="proxd", tmgsyn_params=tmgsyn_params, netcon_params=netcon_params)

        # GC -> BC
        tmgsyn_params = TmgSynParams(tau_1=8.7, tau_facilition=500, tau_recovery=0, U=0.1, e=0)
        netcon_params = NetConParams(threshold=10, delay=0.8, weight=2.5e-2)
        self.GC_TO_BC = connect(pre_population=self.GCs, post_population=self.BCs, n_candidates=8, n_synapses=1, target_section_name="proxd", tmgsyn_params=tmgsyn_params, netcon_params=netcon_params)

        # GC -> HC
        tmgsyn_params = TmgSynParams(tau_1=8.7, tau_facilition=500, tau_recovery=0, U=0.1, e=0)
        netcon_params = NetConParams(threshold=10, delay=1.5, weight=2.5e-2)
        self.GC_TO_HC = connect(pre_population=self.GCs, post_population=self.HCs, n_candidates=24, n_synapses=1, target_section_name="proxd", tmgsyn_params=tmgsyn_params, netcon_params=netcon_params)

        # MC -> MC
        tmgsyn_params = TmgSynParams(tau_1=2.2, tau_facilition=0, tau_recovery=0, U=1, e=0)
        netcon_params = NetConParams(threshold=10, delay=2, weight=5e-4)
        self.MC_TO_MC = connect(pre_population=self.MCs, post_population=self.MCs, n_candidates=24, n_synapses=3, target_section_name="proxd", tmgsyn_params=tmgsyn_params, netcon_params=netcon_params)

        # MC -> BC
        tmgsyn_params = TmgSynParams(tau_1=2, tau_facilition=0, tau_recovery=0, U=1, e=0)
        netcon_params = NetConParams(threshold=10, delay=3, weight=3e-4)
        self.MC_TO_BC = connect(pre_population=self.MCs, post_population=self.BCs, n_candidates=12, n_synapses=1, target_section_name="proxd", tmgsyn_params=tmgsyn_params, netcon_params=netcon_params)

        # MC -> HC
        tmgsyn_params = TmgSynParams(tau_1=6.2, tau_facilition=0, tau_recovery=0, U=1, e=0)
        netcon_params = NetConParams(threshold=10, delay=3, weight=2e-4)
        self.MC_TO_HC = connect(pre_population=self.MCs, post_population=self.HCs, n_candidates=20, n_synapses=2, target_section_name="midd", tmgsyn_params=tmgsyn_params, netcon_params=netcon_params)

        # BC -> GC
        tmgsyn_params = TmgSynParams(tau_1=20, tau_facilition=0, tau_recovery=0, U=1, e=-70)
        netcon_params = NetConParams(threshold=10, delay=0.85, weight=1.2e-3)
        self.BC_TO_GC = connect(pre_population=self.BCs, post_population=self.GCs, n_candidates=560, n_synapses=400, target_section_name="soma", tmgsyn_params=tmgsyn_params, netcon_params=netcon_params)

        # BC -> MC
        tmgsyn_params = TmgSynParams(tau_1=3.3, tau_facilition=0, tau_recovery=0, U=1, e=-70)
        netcon_params = NetConParams(threshold=10, delay=1.5, weight=1.5e-3)
        self.BC_TO_MC = connect(pre_population=self.BCs, post_population=self.MCs, n_candidates=28, n_synapses=3, target_section_name="proxd", tmgsyn_params=tmgsyn_params, netcon_params=netcon_params)

        # BC -> BC
        tmgsyn_params = TmgSynParams(tau_1=1.8, tau_facilition=0, tau_recovery=0, U=1, e=-70)
        netcon_params = NetConParams(threshold=10, delay=0.8, weight=7.6e-3)
        self.BC_TO_BC = connect(pre_population=self.BCs, post_population=self.BCs, n_candidates=12, n_synapses=2, target_section_name="proxd", tmgsyn_params=tmgsyn_params, netcon_params=netcon_params)

        # HC -> GC
        tmgsyn_params = TmgSynParams(tau_1=20, tau_facilition=0, tau_recovery=0, U=1, e=-70)
        netcon_params = NetConParams(threshold=10, delay=3.8, weight=6e-3)
        self.HC_TO_GC = connect(pre_population=self.HCs, post_population=self.GCs, n_candidates=2000, n_synapses=640, target_section_name="dd", tmgsyn_params=tmgsyn_params, netcon_params=netcon_params)

        # HC -> MC
        tmgsyn_params = TmgSynParams(tau_1=6, tau_facilition=0, tau_recovery=0, U=1, e=-70)
        netcon_params = NetConParams(threshold=10, delay=1, weight=1.5e-3)
        # TODO: target_section_name="mid1d", "mid2d"
        self.HC_TO_MC = connect(pre_population=self.HCs, post_population=self.MCs, n_candidates=60, n_synapses=4, target_section_name="mid1d", tmgsyn_params=tmgsyn_params, netcon_params=netcon_params)

        # HC -> BC
        tmgsyn_params = TmgSynParams(tau_1=5.8, tau_facilition=0, tau_recovery=0, U=1, e=-70)
        netcon_params = NetConParams(threshold=10, delay=1.6, weight=5e-4)
        self.HC_TO_BC = connect(pre_population=self.HCs, post_population=self.BCs, n_candidates=24, n_synapses=4, target_section_name="ddend", tmgsyn_params=tmgsyn_params, netcon_params=netcon_params)

        self.connections = [self.GC_TO_MC, self.GC_TO_BC, self.GC_TO_HC, self.MC_TO_MC, self.MC_TO_BC, self.MC_TO_HC, self.BC_TO_GC, self.BC_TO_MC, self.BC_TO_BC, self.HC_TO_GC, self.HC_TO_MC, self.HC_TO_BC]

        self.PP_TO_GC_vecstims = []
        self.PP_TO_BC_vecstims = []

    def evoke_GC(self, temporal_pattern: list[float], spatial_pattern: list[int], weight: float):
        # PP -> GC
        tmgsyn_params = TmgSynParams(tau_1=10, tau_facilition=0, tau_recovery=0, U=1, e=0)
        netcon_params = NetConParams(threshold=10, delay=1, weight=weight)
        connections, vecstim = evoke(population=self.GCs, temporal_pattern=temporal_pattern, spatial_pattern=spatial_pattern, target_section_name="midd", tmgsyn_params=tmgsyn_params, netcon_params=netcon_params)

        self.PP_TO_GC_vecstims.append(vecstim)
        self.connections.append(connections)

    def evoke_BC(self, temporal_pattern: list[float], spatial_pattern: list[int], weight: float):
        # PP -> BC
        tmgsyn_params = TmgSynParams(tau_1=6.3, tau_facilition=0, tau_recovery=0, U=1, e=0)
        netcon_params = NetConParams(threshold=10, delay=1, weight=weight)
        connections, vecstim = evoke(population=self.BCs, temporal_pattern=temporal_pattern, spatial_pattern=spatial_pattern, target_section_name="proxd", tmgsyn_params=tmgsyn_params,netcon_params=netcon_params)
    
        self.PP_TO_BC_vecstims.append(vecstim)
        self.connections.append(connections)