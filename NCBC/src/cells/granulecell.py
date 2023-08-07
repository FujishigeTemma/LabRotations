import os

from .cell import Cell


class GranuleCell(Cell):
    name = "GlanuleCell"

    def _setup_morphology(self):
        self.add_soma(name="soma", diameter=16.8, L=16.8)
        self.add_dendrites(name="dend_1", n_section=4, section_names=["gcld", "proxd", "midd", "dd"], diameters=[3, 3, 3, 3], Ls=[50, 150, 150, 150], soma_location=1)
        self.add_dendrites(name="dend_2", n_section=4, section_names=["gcld", "proxd", "midd", "dd"], diameters=[3, 3, 3, 3], Ls=[50, 150, 150, 150], soma_location=1)

    def _setup_biophysics(self):
        self.load_biophysics_from_file(os.path.join(os.path.dirname(__file__), "granulecell_parameters.tsv"))
