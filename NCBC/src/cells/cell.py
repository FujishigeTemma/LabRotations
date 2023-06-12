from typing import List

import numpy as np
from neuron import h

h.load_file("stdrun.hoc")

class Cell:
    def __init__(self, id: int):
        self._id = id
        self.sections = []
        self.dendrites = []
        self._setup_morphology()
        self._setup_biophysics()

    def add_soma(self, name: str, diameter: float, L: float):
        if hasattr(self, "soma"):
            raise AttributeError("soma already exists")

        self.soma = h.Section(name=name)
        self.soma.diam = diameter
        self.soma.L = L
        self.sections.append(self.soma)

    def add_dendrite(self, name: str, n_section: int, section_names: List[str], diameters: List[float], Ls: List[float], soma_location: float):
        if not hasattr(self, "soma"):
            raise AttributeError("soma does not exist")
        if len(section_names) != n_section or len(diameters) != n_section or len(Ls) != n_section:
            raise ValueError("n_section does not match the length of other parameters")
        if soma_location < 0 or soma_location > 1:
            raise ValueError("soma_location must be between 0 and 1")

        parent_section = self.soma
        for i in range(n_section):
            dendrite = h.Section(name=name + "_" + section_names[i])
            dendrite.L = Ls[i]
            dendrite.diam = diameters[i]
            dendrite.connect(parent_section(soma_location if i == 0 else 1))
            self.sections.append(dendrite)
            self.dendrites.append(dendrite)
            parent_section = dendrite

    def __repr__(self):
        return "{}[{}]".format(self.name, self._id)

    def get_segs_by_name(self, name):
        """Returns a list of sections whose .name matches the name parameter.

        Parameters
        ----------
        name - str or list of str
            The names to gets

        Returns
        -------
        result - list
            List of sections whose .name attribute matches the name parameter

        Use cases
        ---------
        >>> self.get_segs_by_name('proxd')
        Returns segments named 'proxd'
        """

        if "all" in name:
            return list(self.sections)

        result = []
        if type(name) == str:
            for section in self.sections:
                if section.name().endswith(name):
                    result.append(section)
        else:
            for name in name:
                for section in self.sections:
                    if section.name().endswith(name):
                        result.append(name)

        return np.array(result, dtype=np.dtype(object))

    def insert_mechs(self, parameters):
        """Inserts the parameters into the section of the cells.
        See ouropy.parameters

        Parameters
        ----------
        parameters - ouropy.parameters.Parameter or ParameterSet
            A parameter or parameterset contains the mechanism, the segment and
            the value to assign.

        Returns
        -------
        None

        Use Cases
        ---------
        >>> import ouropy.parameters
        >>> myParameters = ouropy.parameters.read_parameters(filename)
        >>> self.insert_mechs(myParameters)
        Insert the parameters loaded from filename into self. See
        ouropy.parameters for details.
        """
        mechanisms = parameters.get_mechs()

        for x in mechanisms.keys():
            sections = self.get_segs_by_name(x)
            for y in sections:
                for z in mechanisms[x]:
                    y.insert(z)

        for x in parameters:
            sections = self.get_segs_by_name(x.sec_name)
            for y in sections:
                setattr(y, x.mech_name, x.value)
