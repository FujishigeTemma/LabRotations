import csv
from typing import List

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

    def add_dendrites(self, name: str, n_section: int, section_names: List[str], diameters: List[float], Ls: List[float], soma_location: float):
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

    def get_sections_by_name(self, name: str):
        if name == "all":
            return self.sections
        sections = []
        for section in self.sections:
            if section.name().endswith(name):
                sections.append(section)
        return sections

    def load_biophysics_from_file(self, path: str):
        parameters: List[Parameter] = []
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

                parameters.append(Parameter(attribute_name, section_name, value))

        mechanisms_for_each_section = {}
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

class Parameter:
    def __init__(self, attribute_name: str, section_name: str, value: float):
        self.attribute_name = attribute_name
        self.section_name = section_name
        self.value = value

    def __repr__(self):
        return f'Parameter({self.attribute_name}, {self.section_name}, {self.value})'

    def __str__(self):
        return f'attribute: {self.attribute_name}, section: {self.section_name}, value: {self.value}'