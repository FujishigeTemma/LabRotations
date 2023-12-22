import flax.linen as nn
import jax
import jax.numpy as jnp
from jax import random

layers = [32, 64, 128, 256, 512, 1024]


class Encoder(nn.Module):
    @nn.compact
    def __call__(self, x: jax.Array, train: bool) -> tuple[jax.Array, jax.Array]:
        for features in layers:
            x = nn.Conv(features, kernel_size=(2, 2), strides=2, use_bias=False)(x)
            x = nn.BatchNorm(use_running_average=not train)(x)
            x = nn.leaky_relu(x)

        x = x.reshape((x.shape[0], -1))

        mean = nn.Dense(features=200)(x)
        logvar = nn.Dense(features=200)(x)

        return mean, logvar


class Decoder(nn.Module):
    @nn.compact
    def __call__(self, z: jax.Array, train: bool) -> jax.Array:
        z = nn.Dense(features=4096)(z)

        z = z.reshape((z.shape[0], 1, 1, 4096))

        for features in reversed(layers):
            z = nn.ConvTranspose(features, kernel_size=(2, 2), strides=(2, 2), use_bias=False)(z)
            z = nn.BatchNorm(use_running_average=not train)(z)
            z = nn.leaky_relu(z)

        z = nn.ConvTranspose(1, kernel_size=(2, 2), strides=(2, 2))(z)
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
    std = jnp.exp(0.5 * logvar)
    eps = random.normal(rng, logvar.shape)
    return mean + eps * std
