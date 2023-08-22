import numpy as np
from neuron import h
from neuron.units import mV


def setup(seed: int):
    np.random.seed(seed)

    h.load_file("stdrun.hoc")

    h.cvode.active(0)

    dt = 0.1
    h.steps_per_ms = 1.0 / dt


def run(warmup: int, duration: int):
    h.finitialize(-60 * mV)

    h.t = -warmup
    h.secondorder = 0
    h.dt = 10
    while h.t < -100:
        h.fadvance()

    h.secondorder = 2
    h.t = 0
    h.dt = 0.1
    h.frecord_init()
    while h.t < duration:
        h.fadvance()
