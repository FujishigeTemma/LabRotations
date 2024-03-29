# ruff: noqa: F401
import click

from .reconstruct import reconstruct
from .train import train


@click.group()
def vae():
    pass


vae.add_command(train)
vae.add_command(reconstruct)
