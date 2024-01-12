import os
from dataclasses import dataclass
from typing import Any, Literal

import click
import input_pipeline
import jax
import jax.numpy as jnp
import numpy as np
import optax
import orbax.checkpoint as ocp
import tensorflow_datasets as tfds
import tomllib
import tqdm
from flax.linen import tabulate
from flax.training import orbax_utils, train_state
from jax import random

import wandb

from .model import IMAGE_SIZE, VAE

DEVICE_COUNT = jax.local_device_count()
BATCH_SIZE = 64 * DEVICE_COUNT
INPUT_SHAPE = (BATCH_SIZE, IMAGE_SIZE, IMAGE_SIZE, 3)


class TrainState(train_state.TrainState):
    batch_stats: Any


@jax.vmap
def mean_squared_error(y: jax.Array, y_target: jax.Array):
    return jnp.square(y - y_target).mean()


@jax.vmap
def kl_divergence(mean: jax.Array, logvar: jax.Array):
    return -0.5 * jnp.sum(1 + logvar - jnp.square(mean) - jnp.exp(logvar))


@jax.jit
def train_step(rng: random.KeyArray, state: TrainState, batch: jax.Array):
    rng, subrng = random.split(rng)

    def loss_fn(params):
        (output, (mean, logvar)), updates = VAE().apply(
            {"params": params, "batch_stats": state.batch_stats},
            batch,
            rngs={"reparameterize": subrng},
            mutable=["batch_stats"],
        )
        mse_loss = mean_squared_error(output, batch).mean()
        kld_loss = kl_divergence(mean, logvar).mean()  # type: ignore
        # loss = mse_loss + kld_loss
        loss = mse_loss
        return loss, (output, mse_loss, kld_loss, updates)

    grad_fn = jax.value_and_grad(loss_fn, has_aux=True)
    (loss, (output, mse_loss, kld_loss, updates)), grads = grad_fn(state.params)

    state = state.apply_gradients(grads=grads)
    state = state.replace(batch_stats=updates["batch_stats"])

    metrics = {
        "loss": loss,
        "mse_loss": mse_loss,
        "kld_loss": kld_loss,
    }

    return state, output, metrics


@dataclass
class Config:
    dataset: Literal["mnist", "cifar100", "imagenet2012"]
    n_epochs: int
    checkpoint_dir: str


def validate_config(ctx, param, value):
    if not os.path.exists(value):
        raise click.BadParameter(f"Config file {value} does not exist.")
    with open(value, "rb") as f:
        config = tomllib.load(f)

    if config["dataset"] not in ["mnist", "cifar100", "imagenet2012"]:
        raise click.BadParameter(f"Dataset {config['dataset']} is not supported.")

    for key in Config.__annotations__.keys():
        if key not in config:
            raise click.BadParameter(f"Config file does not contain {key}.")
        if (key.endswith("_path") or key.endswith("_dir")) and not os.path.exists(config[key]):
            raise click.BadParameter(f"{key} {config[key]} does not exist.")

    return Config(**config)


@click.command()
@click.option("--config", "-c", required=True, type=click.UNPROCESSED, callback=validate_config)
def train(config: Config):
    wandb.init(project="VAE", config=config.__dict__)

    rng = random.key(0)
    rng, *rngs = random.split(rng, 3)

    checkpointer = ocp.AsyncCheckpointer(ocp.PyTreeCheckpointHandler(use_ocdbt=True))

    options = ocp.CheckpointManagerOptions(max_to_keep=5, create=True)
    checkpoint_dir = os.path.join(config.checkpoint_dir, "vae", config.dataset)
    checkpoint_manager = ocp.CheckpointManager(checkpoint_dir, checkpointer, options)

    vae = VAE()

    init_rng = {"params": rngs[0], "reparameterize": rngs[1]}
    init_data = jnp.ones(INPUT_SHAPE, jnp.float32)

    tabulate_fn = tabulate(vae, init_rng, compute_flops=True, compute_vjp_flops=True)
    print(tabulate_fn(init_data))

    best_step = checkpoint_manager.best_step()
    if best_step is not None:
        checkpoint = checkpoint_manager.restore(best_step)
        state = checkpoint["state"]
        params = state["params"]
        batch_stats = state["batch_stats"]
    else:
        variables = vae.init(init_rng, init_data)
        params = variables["params"]
        batch_stats = variables["batch_stats"]

    state = TrainState.create(apply_fn=vae.apply, params=params, batch_stats=batch_stats, tx=optax.adam(1e-3))

    ds_builder = tfds.builder(config.dataset)
    ds_builder.download_and_prepare()

    train_ds = input_pipeline.build_train_set(BATCH_SIZE, ds_builder)

    steps_per_epoch = ds_builder.info.splits[tfds.Split.TRAIN].num_examples // BATCH_SIZE  # type: ignore

    iterator = tqdm.trange(best_step + 1 if best_step else 0, config.n_epochs, desc="Epoch")
    for epoch in iterator:
        epoch_metrics = {}

        rng, *rngs = random.split(rng, steps_per_epoch + 1)
        for step in tqdm.trange(steps_per_epoch, desc="Batch", leave=False):
            batch = next(train_ds)
            state, output, metrics = train_step(rngs[step], state, batch)

            epoch_metrics = {key: epoch_metrics.get(key, 0.0) + value for key, value in metrics.items()}

            if step == steps_per_epoch - 1:
                wandb.log(
                    {
                        "input": wandb.Image(np.array(batch[0] * 255.0)),
                        "output": wandb.Image(np.array(output[0] * 255.0)),
                    },
                    step=epoch,
                )

        epoch_metrics = {key: value / steps_per_epoch for key, value in epoch_metrics.items()}
        wandb.log(epoch_metrics, step=epoch)
        iterator.set_postfix(loss=epoch_metrics["loss"])

        checkpoint = {"state": state}
        save_args = orbax_utils.save_args_from_target(checkpoint)
        checkpoint_manager.save(epoch, checkpoint, save_kwargs={"save_args": save_args}, force=True)

    checkpoint_manager.wait_until_finished()
