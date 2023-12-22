import click
from vae import reconstruct, train


@click.group()
def cli():
    pass


cli.add_command(train)
cli.add_command(reconstruct)

if __name__ == "__main__":
    cli()
