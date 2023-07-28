import click

from dentate_gyrus import simulate_dentate_gyrus
from gap_junction import simulate_EPSP_propagation, simulate_gap_junction


@click.group()
def cli():
    pass

cli.add_command(simulate_gap_junction)
cli.add_command(simulate_EPSP_propagation)
cli.add_command(simulate_dentate_gyrus)

if __name__ == "__main__":
    cli()