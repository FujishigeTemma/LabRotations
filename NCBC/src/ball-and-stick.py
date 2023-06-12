import matplotlib.pyplot as plt
from cell import Cell
from neuron import gui, h  # noqa: F401
from neuron.units import ms, mV

h.load_file("stdrun.hoc")


class BallAndStick(Cell):
    name = "BallAndStick"

    def _setup_morphology(self) -> None:
        self.soma = h.Section(name="soma", cell=self)
        self.dendrite = h.Section(name="dendrite", cell=self)

        self.dendrite.connect(self.soma)

        self.soma.L = self.soma.diam = 12.6157
        self.dendrite.L = 200
        self.dendrite.diam = 1

    def _setup_biophysics(self) -> None:
        for sec in self.all:
            sec.Ra = 100
            sec.cm = 1

        self.soma.insert("hh")
        for seg in self.soma:
            seg.hh.gnabar = 0.12
            seg.hh.gkbar = 0.036
            seg.hh.gl = 0.0003
            seg.hh.el = -54.3

        self.dendrite.insert("pas")
        for seg in self.dendrite:
            seg.pas.g = 0.001
            seg.pas.e = -65


cell = BallAndStick(0)


stimulus = h.IClamp(cell.dendrite(1))

stimulus.delay = 5
stimulus.dur = 1
stimulus.amp = 0.1

soma_v = h.Vector().record(cell.soma(0.5)._ref_v)
dendrite_v = h.Vector().record(cell.dendrite(0.5)._ref_v)
t = h.Vector().record(h._ref_t)

fig, ax = plt.subplots()

amps = [0.075 * i for i in range(4, 5)]
colors = ["green", "blue", "red", "black"]

for amp, color in zip(amps, colors):
    stimulus.amp = amp
    for cell.dendrite.nseg, line_width in [(1, 2), (101, 1)]:
        h.finitialize(-65 * mV)
        h.continuerun(25 * ms)
        ax.plot(t, soma_v, color=color, label=f"{stimulus.amp:.3} nA" if cell.dendrite.nseg == 1 else None, lw=line_width)
        ax.plot(t, dendrite_v, color=color, ls="--", lw=line_width)

ax.set(xlabel="t (ms)", ylabel="v (mV)")
ax.legend()

plt.show()
