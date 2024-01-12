import os
from dataclasses import dataclass

import click
import input_pipeline
import matplotlib.pyplot as plt
import orbax.checkpoint as ocp
import tensorflow_datasets as tfds
import tomllib
from jax import random

from .model import Autoencoder


@dataclass
class Config:
    checkpoint_dir: str
    output_dir: str


def validate_config(ctx, param, value):
    if not os.path.exists(value):
        raise click.BadParameter(f"Config file {value} does not exist.")
    with open(value, "rb") as f:
        config = tomllib.load(f)

    for key in Config.__annotations__.keys():
        if key not in config:
            raise click.BadParameter(f"Config file does not contain {key}.")
        if (key.endswith("_path") or key.endswith("_dir")) and not os.path.exists(config[key]):
            raise click.BadParameter(f"{key} {config[key]} does not exist.")

    return Config(**config)


@click.command()
@click.option("--config", "-c", required=True, type=click.UNPROCESSED, callback=validate_config)
def reconstruct(config: Config):
    rng = random.key(0)

    checkpointer = ocp.AsyncCheckpointer(ocp.PyTreeCheckpointHandler(use_ocdbt=True))

    options = ocp.CheckpointManagerOptions(max_to_keep=5, create=True)
    checkpoint_manager = ocp.CheckpointManager(
        os.path.join(config.checkpoint_dir, "autoencoder"), checkpointer, options
    )

    best_step = checkpoint_manager.best_step()
    if best_step is None:
        raise ValueError("No checkpoint found.")
    checkpoint = checkpoint_manager.restore(best_step)

    state = checkpoint["state"]

    ds_builder = tfds.builder("mnist")
    ds_builder.download_and_prepare()

    N_ROWS = 5

    test_ds = input_pipeline.build_test_set(N_ROWS * N_ROWS, ds_builder)
    batch = next(test_ds)

    output = Autoencoder().apply(
        {"params": state["params"], "batch_stats": state["batch_stats"]},
        x=batch,
        train=False,
        rngs={"reparameterize": rng},
    )

    fig, axes = plt.subplots(N_ROWS, N_ROWS * 2)
    for i in range(N_ROWS):
        for j in range(N_ROWS):
            axes[i][j * 2].imshow(batch[i * N_ROWS + j], cmap="gray")
            axes[i][j * 2 + 1].imshow(output[i * N_ROWS + j], cmap="gray")

            axes[i][j * 2].axis("off")
            axes[i][j * 2 + 1].axis("off")

    fig.tight_layout()
    fig.savefig(os.path.join(config.output_dir, "reconstruction.png"))
