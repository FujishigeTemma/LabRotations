from .population import Connection, Population


class Network:
    name: str
    populations: list[Population]
    connections: list[list[Connection]]
