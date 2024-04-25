from dataclasses import dataclass

import numpy as np
from cells import Cell
from neuron import h


class Population:
    voltage_recordings: list

    def __init__(self, index: int, cell_type: type[Cell], n_cells: int):
        self.id = f"Population({cell_type.name})#{index}"
        self.cell_type = cell_type
        self.cells = [cell_type(i) for i in range(n_cells)]
        self.voltage_recordings = []
        self.action_potential_recordings = []

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id


def find_nearest_points(n: int, m: int, k: int):
    """
    arrange the `n`,`m` of cells in a circle and find the `k`-nearest point indices for each cell
    NOTE: first cells are positioned at 0 degrees and the angle increases anti-clockwise
    """

    # Calculate the angles for each point on A and B
    angles_A = np.array([2 * np.pi * i / n for i in range(n)])
    angles_B = np.array([2 * np.pi * i / m for i in range(m)])

    nearest_points = np.empty((n, k), dtype=np.int32)

    for i, angle in enumerate(angles_A):
        # Calculate the difference in angles from the point on A to each point on B
        angle_differences = np.abs(angles_B - angle)

        # Since we are dealing with a circle, an angle difference > 180 degrees could be smaller
        # if calculated the other way around (360 - angle difference)
        angle_differences = np.minimum(angle_differences, 2 * np.pi - angle_differences)

        # Get the indices of the points on B that are closest to the point on A
        nearest_points_indices = np.argsort(angle_differences)[:k]

        nearest_points[i] = nearest_points_indices

    return nearest_points


@dataclass
class TmgSynParams:
    tau_1: float
    tau_facilition: float
    tau_recovery: float
    U: float
    e: float


@dataclass
class NetConParams:
    threshold: float
    delay: float
    weight: float


@dataclass
class Connection:
    synapse: object
    netcon: object


def connect(
    pre_population: Population, post_population: Population, n_candidates: int, n_synapses: int, target_section_name: str, tmgsyn_params: TmgSynParams, netcon_params: NetConParams
) -> tuple[list[Connection], np.ndarray]:
    if n_candidates > len(post_population.cells):
        raise ValueError("n_candidate must be smaller than or equal to the number of cells in post_population")
    if n_synapses > n_candidates:
        raise ValueError("n_synapse must be smaller than or equal to n_candidate")

    # record adjacent matrix
    A = np.zeros((len(pre_population.cells), len(post_population.cells)), dtype=np.int32)

    each_nearest_points = find_nearest_points(len(pre_population.cells), len(post_population.cells), n_candidates)

    connections: list[Connection] = []
    for pre_cell_index, nearest_points in enumerate(each_nearest_points):
        chosen_cells = np.random.choice(nearest_points, n_synapses, replace=False)
        for post_cell_index in chosen_cells:
            A[pre_cell_index, post_cell_index] = 1

            target_sections = post_population.cells[post_cell_index].get_sections_by_name(target_section_name)
            chosen_section = np.random.choice(target_sections)

            synapse = h.tmgsyn(chosen_section(0.5))
            synapse.tau_1 = tmgsyn_params.tau_1
            synapse.tau_facilition = tmgsyn_params.tau_facilition
            synapse.tau_recovery = tmgsyn_params.tau_recovery
            synapse.U = tmgsyn_params.U
            synapse.e = tmgsyn_params.e

            pre_soma = pre_population.cells[pre_cell_index].soma
            netcon = h.NetCon(pre_soma(0.5)._ref_v, synapse, sec=pre_soma)
            netcon.threshold = netcon_params.threshold
            netcon.delay = netcon_params.delay
            netcon.weight[0] = netcon_params.weight

            connections.append(Connection(synapse, netcon))

    return connections, A


@dataclass
class GapJunction:
    pre: object
    post: object


def connect_gap(pre_population: Population, post_population: Population, n_candidates: int, n_synapses: int) -> list[GapJunction]:
    if n_candidates > len(post_population.cells):
        raise ValueError("n_candidate must be smaller than or equal to the number of cells in post_population")
    if n_synapses > n_candidates:
        raise ValueError("n_synapse must be smaller than or equal to n_candidate")

    each_nearest_points = find_nearest_points(len(pre_population.cells), len(post_population.cells), n_candidates)

    connections: list[GapJunction] = []
    for pre_cell_index, nearest_points in enumerate(each_nearest_points):
        chosen_cells = np.random.choice(nearest_points, n_synapses, replace=False)
        for post_cell_index in chosen_cells:
            pre = pre_population.cells[pre_cell_index]
            post = post_population.cells[post_cell_index]

            pre_gap = h.gap(pre.dendrites[1](0.5))
            post_gap = h.gap(post.dendrites[1](0.5))

            pre_gap.r = 6e2
            pre_gap.delay = 5
            post_gap.r = 6e2
            post_gap.delay = 5

            h.setpointer(post.dendrites[1](0.5)._ref_v, "v_pair", pre_gap)
            h.setpointer(pre.dendrites[1](0.5)._ref_v, "v_pair", post_gap)

            connections.append(GapJunction(pre_gap, post_gap))

    return connections


def evoke(population: Population, temporal_pattern: list[float], spatial_pattern: list[int], target_section_name: str, tmgsyn_params: TmgSynParams, netcon_params: NetConParams):
    evoked_cells = np.array(population.cells)[spatial_pattern]

    vecstim = h.VecStim()
    pattern = h.Vector(temporal_pattern)
    vecstim.play(pattern)

    connections = []
    for cell in evoked_cells:
        target_sections = cell.get_sections_by_name(target_section_name)

        for section in target_sections:
            synapse = h.tmgsyn(section(0.5))
            synapse.tau_1 = tmgsyn_params.tau_1
            synapse.tau_facilition = tmgsyn_params.tau_facilition
            synapse.tau_recovery = tmgsyn_params.tau_recovery
            synapse.U = tmgsyn_params.U
            synapse.e = tmgsyn_params.e

            netcon = h.NetCon(vecstim, synapse)
            netcon.threshold = netcon_params.threshold
            netcon.delay = netcon_params.delay
            netcon.weight[0] = netcon_params.weight

            connections.append(Connection(synapse, netcon))

    return connections, (vecstim, pattern)
