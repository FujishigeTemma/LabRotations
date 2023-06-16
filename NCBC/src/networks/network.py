class Network:
    name: str

    def __init__(self, id):
        self.id = id
        self.cells = []
        self.connections = []
        self.stimuli = []