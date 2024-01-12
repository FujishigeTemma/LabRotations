# ruff: noqa: F401
import click

from .reconstruct import reconstruct
from .train import train


@click.group()
def autoencoder():
    pass


autoencoder.add_command(train)
autoencoder.add_command(reconstruct)
