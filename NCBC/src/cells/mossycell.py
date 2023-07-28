import os

from .cell import Cell


class MossyCell(Cell):
    name = "MossyCell"

    def _setup_morphology(self):
        self.add_soma(name="soma", diameter=20, L=20)
        self.add_dendrites(name="dend_1", n_section=4, section_names=["proxd", "mid1d", "mid2d", "dd"], diameters=[5.78, 4, 2.5, 1], Ls=[50, 50, 50, 50], soma_location=1)
        self.add_dendrites(name="dend_2", n_section=4, section_names=["proxd", "mid1d", "mid2d", "dd"], diameters=[5.78, 4, 2.5, 1], Ls=[50, 50, 50, 50], soma_location=1)
        self.add_dendrites(name="dend_3", n_section=4, section_names=["proxd", "mid1d", "mid2d", "dd"], diameters=[5.78, 4, 2.5, 1], Ls=[50, 50, 50, 50], soma_location=0)
        self.add_dendrites(name="dend_4", n_section=4, section_names=["proxd", "mid1d", "mid2d", "dd"], diameters=[5.78, 4, 2.5, 1], Ls=[50, 50, 50, 50], soma_location=0)
    
    def _setup_biophysics(self):
        self.load_biophysics_from_file(os.path.join(os.path.dirname(__file__), "mossycell_parameters.tsv"))