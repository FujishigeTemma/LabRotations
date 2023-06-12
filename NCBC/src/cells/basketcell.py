import os

from .cell import Cell


class BasketCell(Cell):
    name = "BasketCell"

    def _setup_morphology(self):
        self.add_soma(name="soma", diameter=15, L=20)
        self.add_dendrites(name="basal_1", n_section=4, section_names=["proxd", "mid1", "mid2", "ddend"], diameters=[4, 3, 2, 1], Ls=[50, 50, 50, 50], soma_location=0)
        self.add_dendrites(name="basal_2", n_section=4, section_names=["proxd", "mid1", "mid2", "ddend"], diameters=[4, 3, 2, 1], Ls=[50, 50, 50, 50], soma_location=0)
        self.add_dendrites(name="apical_1", n_section=4, section_names=["proxd", "mid1", "mid2", "ddend"], diameters=[4, 3, 2, 1], Ls=[75, 75, 75, 75], soma_location=1.0)
        self.add_dendrites(name="apical_2", n_section=4, section_names=["proxd", "mid1", "mid2", "ddend"], diameters=[4, 3, 2, 1], Ls=[75, 75, 75, 75], soma_location=1.0)

    def _setup_biophysics(self):
        self.load_biophysics_from_file(os.path.join(os.path.dirname(__file__), "basketcell_parameters.tsv"))
