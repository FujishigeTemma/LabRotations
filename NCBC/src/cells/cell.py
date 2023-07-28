import csv
from collections.abc import Iterator
from dataclasses import dataclass

from neuron import h


class Cell:
    """
    Base class for all cells.

    Usage
    -----
    >>> from cells import Cell
    >>> 
    >>> class MyCell(Cell):
    >>>     name = "mycell"
    >>>
    >>>     def _setup_morphology(self):
    >>>         self.add_soma(name="soma", diameter=15, L=20)
    >>>         self.add_dendrites(name="dend", n_section=3, section_names=["proximal", "middle", "distal"], diameters=[3, 2, 1], Ls=[50, 50, 50], soma_location=0)
    >>>     def _setup_biophysics(self):
    >>>         self.load_biophysics_from_file("path/to/biophysics.tsv")
    >>>
    >>> cell = MyCell(0)

    Attributes
    ----------
    id : int
        ID of the cell.
    name : str
        Name of the cell.
    sections : list[h.Section]
        List of all sections.
    dendrites : list[h.Section]
        List of dendrites.

    Methods
    -------
    add_soma(name: str, diameter: float, L: float) -> None
        Add a soma to the cell.
    add_dendrites(name: str, n_section: int, section_names: list[str], diameters: list[float], Ls: list[float], soma_location: float) -> None
        Add dendrites to the cell.
    get_sections_by_name(name: str) -> list[h.Section]
        Get sections by name.
    load_biophysics_from_file(path: str) -> None
        Load biophysics from a tsv file.
        Syntax of the tsv file is as follows:
        ```
        attribute_name    section_name    value
        ```
    """
    name: str

    def __init__(self, index: int):
        self.id = f"{self.name}#{index}"
        self.sections = []
        self.dendrites = []
        self._setup_morphology()
        self._setup_biophysics()
    
    def _setup_morphology(self) -> None:
        raise NotImplementedError("_setup_morphology must be implemented")

    def _setup_biophysics(self) -> None:
        raise NotImplementedError("_setup_biophysics must be implemented")

    def add_soma(self, name: str, diameter: float, L: float):
        if hasattr(self, "soma"):
            raise AttributeError("soma already exists")

        self.soma = h.Section(name=name)
        self.soma.diam = diameter
        self.soma.L = L
        self.sections.append(self.soma)

    def add_dendrites(self, name: str, n_section: int, section_names: list[str], diameters: list[float], Ls: list[float], soma_location: float):
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
    
    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id

    def get_sections_by_name(self, name: str):
        if name == "all":
            return self.sections
        sections = []
        for section in self.sections:
            if section.name().endswith(name):
                sections.append(section)
        return sections

    def load_biophysics_from_file(self, path: str):
        parameters: list[Parameter] = []
        for parameter in parameter_reader(path):
            parameters.append(parameter)

        mechanisms_for_each_section: dict[str, list[str]] = {}
        for parameter in parameters:
            if mechanisms_for_each_section.get(parameter.section_name) is None:
                mechanisms_for_each_section[parameter.section_name] = []
            
            splited = parameter.attribute_name.split("_")
            if len(splited) == 2:
                mechanisms_for_each_section[parameter.section_name].append(splited[1])

        # initialize mechanisms for each section
        for section_name, mechanisms in mechanisms_for_each_section.items():
            sections = self.get_sections_by_name(section_name)
            for section in sections:
                for mechanism in mechanisms:
                    section.insert(mechanism)
        
        # set section parameters
        for parameter in parameters:
            sections = self.get_sections_by_name(parameter.section_name)
            for section in sections:
                setattr(section, parameter.attribute_name, parameter.value)

@dataclass(frozen=True)
class Parameter:
    attribute_name: str
    section_name: str
    value: float

def parameter_reader(path: str) -> Iterator[Parameter]:
    with open(path, "r") as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            if len(row) == 0 or row[0].startswith("#"):
                continue
            if len(row) != 3:
                raise ValueError("Each row must have 3 columns")
            
            attribute_name = row[0]
            section_name = row[1]
            value = float(row[2])
    
            yield Parameter(attribute_name, section_name, value)
