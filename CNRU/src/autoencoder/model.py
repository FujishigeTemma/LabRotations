import flax.linen as nn
import jax

IMAGE_SIZE = 128
N_CHANNELS = 3
LAYERS = [32, 64, 128, 256, 512, 1024]
LATENT_DIM = 200
N_FEATURES = (IMAGE_SIZE // 2 ** len(LAYERS)) ** 2 * LAYERS[-1]


class Encoder(nn.Module):
    @nn.compact
    def __call__(self, x: jax.Array, train: bool) -> jax.Array:
        for features in LAYERS:
            x = nn.Conv(features, kernel_size=(2, 2), strides=2, use_bias=False)(x)
            x = nn.BatchNorm(use_running_average=not train)(x)
            x = nn.leaky_relu(x)

        x = x.reshape((x.shape[0], -1))
        x = nn.Dense(features=LATENT_DIM)(x)

        return x


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


class Autoencoder(nn.Module):
    def setup(self):
        self.encoder = Encoder()
        self.decoder = Decoder()

    def __call__(self, x: jax.Array, train: bool = True):
        z = self.encoder(x, train)
        y = self.decoder(z, train)
        return y
