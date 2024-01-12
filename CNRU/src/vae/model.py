import flax.linen as nn
import jax
import jax.numpy as jnp
from jax import random

IMAGE_SIZE = 128
N_CHANNELS = 3
LAYERS = [32, 64, 128, 256, 512, 1024]
LATENT_DIM = 200
N_FEATURES = (IMAGE_SIZE // 2 ** len(LAYERS)) ** 2 * LAYERS[-1]


class Encoder(nn.Module):
    @nn.compact
    def __call__(self, x: jax.Array, train: bool) -> tuple[jax.Array, jax.Array]:
        for features in LAYERS:
            x = nn.Conv(features, kernel_size=(2, 2), strides=2, use_bias=False)(x)
            x = nn.BatchNorm(use_running_average=not train)(x)
            x = nn.leaky_relu(x)

        x = x.reshape((x.shape[0], -1))

        mean = nn.Dense(features=LATENT_DIM)(x)
        logvar = nn.Dense(features=LATENT_DIM)(x)

        return mean, logvar


class Decoder(nn.Module):
    @nn.compact
    def __call__(self, z: jax.Array, train: bool) -> jax.Array:
        z = nn.Dense(features=N_FEATURES)(z)

        z = z.reshape((z.shape[0], 1, 1, N_FEATURES))

        for features in reversed(LAYERS):
            z = nn.ConvTranspose(features, kernel_size=(2, 2), strides=(2, 2), use_bias=False)(z)
            z = nn.BatchNorm(use_running_average=not train)(z)
            z = nn.leaky_relu(z)

        z = nn.ConvTranspose(N_CHANNELS, kernel_size=(2, 2), strides=(2, 2))(z)
        z = nn.sigmoid(z)

        return z


class VAE(nn.Module):
    def setup(self):
        self.encoder = Encoder()
        self.decoder = Decoder()

    def __call__(self, x: jax.Array, train: bool = True):
        mean, logvar = self.encoder(x, train)
        rng = self.make_rng("reparameterize")
        z = reparameterize(rng, mean, logvar)
        y = self.decoder(z, train)
        return y, (mean, logvar)


def reparameterize(rng: random.KeyArray, mean: jax.Array, logvar: jax.Array):
    logvar_clipped = jnp.clip(logvar, a_min=-10, a_max=10)
    std = jnp.exp(0.5 * logvar_clipped)

    eps = random.normal(rng, logvar.shape)
    eps_clipped = jnp.clip(eps, a_min=-2, a_max=2)

    return mean + eps_clipped * std
