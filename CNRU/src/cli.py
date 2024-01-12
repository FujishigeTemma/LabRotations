import click
from autoencoder import autoencoder
from vae import vae


@click.group()
def cli():
    pass


cli.add_command(autoencoder)
cli.add_command(vae)

if __name__ == "__main__":
    cli()
