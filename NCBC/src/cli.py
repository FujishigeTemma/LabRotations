import click

from gap_junction import simulate_gap_junction


@click.group()
def cli():
    pass

cli.add_command(simulate_gap_junction)

if __name__ == "__main__":
    cli()