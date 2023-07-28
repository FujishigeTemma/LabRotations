import os

from .cell import Cell


class HippCell(Cell):
    name = "HippCell"

    def _setup_morphology(self):
        self.add_soma(name="soma", diameter=15, L=20)
        self.add_dendrites(name="short_1", n_section=3, section_names=["proxd", "midd", "distd"], diameters=[3, 2, 1], Ls=[50, 50, 50], soma_location=0)
        self.add_dendrites(name="short_2", n_section=3, section_names=["proxd", "midd", "distd"], diameters=[3, 2, 1], Ls=[50, 50, 50], soma_location=0)
        self.add_dendrites(name="long_1", n_section=3, section_names=["proxd", "midd", "distd"], diameters=[3, 2, 1], Ls=[75, 75, 75], soma_location=1)
        self.add_dendrites(name="long_2", n_section=3, section_names=["proxd", "midd", "distd"], diameters=[3, 2, 1], Ls=[75, 75, 75], soma_location=1)

    def _setup_biophysics(self):
        self.load_biophysics_from_file(os.path.join(os.path.dirname(__file__), "hippcell_parameters.tsv"))