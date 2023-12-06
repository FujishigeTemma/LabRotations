import timm
from torch import nn
from torchinfo import summary


class Decoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.decoder = nn.Sequential(
            nn.Unflatten(1, (1024, 1, 1)),
            nn.Hardswish(),
            nn.ConvTranspose2d(1024, 512, kernel_size=7, stride=7),
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.ConvTranspose2d(512, 256, kernel_size=2, stride=2),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.ConvTranspose2d(256, 128, kernel_size=2, stride=2),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.ConvTranspose2d(128, 64, kernel_size=2, stride=2),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.ConvTranspose2d(64, 32, kernel_size=2, stride=2),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.ConvTranspose2d(32, 3, kernel_size=2, stride=2),
            nn.Sigmoid(),
        )

    def forward(self, x):
        x = self.decoder(x)
        return x


class AutoEncoder(nn.Module):
    def __init__(self, model_name):
        super().__init__()
        self.encoder = timm.create_model(model_name, pretrained=True, num_classes=0)
        self.decoder = Decoder()

        for param in self.encoder.parameters():
            param.requires_grad = False

        summary(self.decoder, input_size=(32, 1024))
        summary(self.encoder, input_size=(32, 3, 224, 224))

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x

    def encode(self, x):
        x = self.encoder(x)
        return x

    def decode(self, x):
        x = self.decoder(x)
        return x
