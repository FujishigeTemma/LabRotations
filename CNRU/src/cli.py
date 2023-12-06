import click

from finetune import finetune
from reconstruct import reconstruct
from train_decoder import train_decoder


@click.group()
def cli():
    pass


cli.add_command(train_decoder)
cli.add_command(finetune)
cli.add_command(reconstruct)

if __name__ == "__main__":
    cli()
