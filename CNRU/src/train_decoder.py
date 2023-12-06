import os

import click
import tomli
import torch
import torch.nn as nn
import torchvision
import tqdm
from timm.data import create_transform, resolve_model_data_config
from torch.optim import Adam, Optimizer
from torch.utils.data import DataLoader

from autoencoder import AutoEncoder


@click.command()
@click.option("--config-path", "-c", type=str, required=True, help="Path to config file")
def train_decoder(config_path: str):
    with open(config_path, "rb") as f:
        config = tomli.load(f)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = AutoEncoder("mobilenetv3_small_100")
    model.train()
    model.to(device)

    if config.get("resume_from") is not None:
        checkpoint = torch.load(config["checkpoint_dir"])
        model.decoder.load_state_dict(checkpoint["model_state_dict"])

    data_config = resolve_model_data_config(model)
    transform = create_transform(**data_config)

    num_cpus = os.cpu_count() or 1

    root = os.path.join(config["data_dir"], config["dataset_name"])
    if config["dataset_name"] == "ImageNet":
        dataset = torchvision.datasets.ImageNet(root=root, split="train", transform=transform)  # type: ignore
    elif config["dataset_name"] == "CIFAR100":
        dataset = torchvision.datasets.CIFAR100(root=root, train=True, download=True, transform=transform)  # type: ignore
    else:
        raise ValueError(f"Unknown dataset: {config['dataset_name']}")
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True, num_workers=num_cpus, pin_memory=True)

    print(dataset)

    features, labels = next(iter(dataloader))
    print(f"features.shape: {features.shape}")
    print(f"labels.shape: {labels.shape}")

    criterion = nn.MSELoss()
    optimizer = Adam(model.decoder.parameters(), lr=0.01)

    train(config, model, criterion, optimizer, dataloader)


def train(config, model: AutoEncoder, criterion: nn.Module, optimizer: Optimizer, dataloader: DataLoader):
    losses = []

    iterator = tqdm.trange(config["n_epochs"], desc="Epoch")
    for epoch in iterator:
        total_loss = 0.0
        for batch in tqdm.tqdm(dataloader, desc="Batch", leave=False):
            optimizer.zero_grad()
            img, _ = batch
            if torch.cuda.is_available():
                img = img.cuda()
            reconstructed = model(img)
            loss = criterion(reconstructed, img)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        losses.append(total_loss / len(dataloader))
        iterator.set_postfix(loss=losses[-1])

        if (epoch + 1) % 10 == 0:
            torch.save(
                {
                    "epoch": epoch,
                    "model_state_dict": model.decoder.state_dict(),
                    "optimizer_state_dict": optimizer.state_dict(),
                    "loss": total_loss / len(dataloader),
                },
                os.path.join(config["checkpoint_dir"], f"decoder_{epoch + 1}.pth"),
            )
            print(f"Saved checkpoint to {config['checkpoint_dir']}/{epoch + 1}.pth")

    return losses
