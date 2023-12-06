import os
from dataclasses import dataclass

import click
import matplotlib.pyplot as plt
import tomli
import torch
import torchvision
from timm.data import create_transform, resolve_model_data_config
from torch.utils.data import DataLoader

from autoencoder import AutoEncoder


# Transform: Compose(
#                Resize(size=256, interpolation=bicubic, max_size=None, antialias=None)
#                CenterCrop(size=(224, 224))
#                ToTensor()
#                Normalize(mean=tensor([0.4850, 0.4560, 0.4060]), std=tensor([0.2290, 0.2240, 0.2250]))
#            )
def inverse_transform(original_size: tuple[int, int]):
    mean = torch.tensor([0.485, 0.456, 0.406])
    std = torch.tensor([0.229, 0.224, 0.225])

    inverse_normalize = torchvision.transforms.Normalize(mean=-mean / std, std=1 / std)

    padding = torchvision.transforms.Pad(256 - 224)

    resize = torchvision.transforms.Resize(original_size)

    return torchvision.transforms.Compose([inverse_normalize, padding, resize])


def save_fig(images: torch.Tensor, path: str):
    fig, axes = plt.subplots(10, 10, figsize=(10, 10))

    for i in range(images.shape[0]):
        arr = images[i].numpy().transpose((1, 2, 0))
        axes[i // 10, i % 10].imshow(arr)
        axes[i // 10, i % 10].set_title(i + 1, fontsize=12)
        axes[i // 10, i % 10].axis("off")

    fig.tight_layout()
    plt.savefig(path)


@dataclass
class Config:
    checkpoint_path: str
    dataset_name: str
    data_dir: str
    output_dir: str


def validate_config(ctx, param, value):
    if not os.path.exists(value):
        raise click.BadParameter(f"Config file {value} does not exist.")
    with open(value, "rb") as f:
        config = tomli.load(f)

    for key in Config.__annotations__.keys():
        if key not in config:
            raise click.BadParameter(f"Config file does not contain {key}.")
        if (key.endswith("_path") or key.endswith("_dir")) and not os.path.exists(config[key]):
            raise click.BadParameter(f"{key} {config[key]} does not exist.")

    return Config(**config)


@click.command()
@click.option("--config", "-c", required=True, type=click.UNPROCESSED, callback=validate_config)
def reconstruct(config: Config):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = AutoEncoder("mobilenetv3_small_100")
    model.eval()
    model.to(device)

    checkpoint = torch.load(config.checkpoint_path)
    model.decoder.load_state_dict(checkpoint["model_state_dict"])

    num_cpus = os.cpu_count() or 1
    if hasattr(os, "sched_getaffinity"):
        try:
            num_cpus = len(os.sched_getaffinity(0))  # type: ignore
        except Exception:
            pass

    root = os.path.join(config.data_dir, config.dataset_name)
    if config.dataset_name == "ImageNet":
        transform = torchvision.transforms.Compose(
            [
                torchvision.transforms.Resize(size=256, interpolation=torchvision.transforms.InterpolationMode.BICUBIC, max_size=None, antialias=None),
                torchvision.transforms.CenterCrop(size=(224, 224)),
                torchvision.transforms.ToTensor(),
            ]
        )
        dataset = torchvision.datasets.ImageNet(root=root, split="val", transform=transform)
        original_size = (224, 224)
    elif config.dataset_name == "CIFAR100":
        dataset = torchvision.datasets.CIFAR100(root=root, train=False, download=True, transform=torchvision.transforms.ToTensor())  # type: ignore
        original_size = (32, 32)
    else:
        raise ValueError(f"Unknown dataset: {config.dataset_name}")
    dataloader = DataLoader(dataset, batch_size=100, shuffle=False, num_workers=num_cpus, pin_memory=True)

    batch = next(iter(dataloader))
    images, _ = batch

    save_fig(images, os.path.join(config.output_dir, f"{config.dataset_name}_original.png"))

    data_config = resolve_model_data_config(model)
    transform = create_transform(**data_config)

    if config.dataset_name == "ImageNet":
        dataset = torchvision.datasets.ImageNet(root=root, split="val", transform=transform)
        original_size = (224, 224)
    elif config.dataset_name == "CIFAR100":
        dataset = torchvision.datasets.CIFAR100(root=root, train=False, download=True, transform=transform)  # type: ignore
        original_size = (32, 32)
    else:
        raise ValueError(f"Unknown dataset: {config.dataset_name}")
    dataloader = DataLoader(dataset, batch_size=100, shuffle=False, num_workers=num_cpus, pin_memory=True)

    batch = next(iter(dataloader))
    images, _ = batch
    images = images.to(device)
    reconstructed = model(images)
    reconstructed = reconstructed.detach().cpu()
    reconstructed = inverse_transform(original_size)(reconstructed)

    save_fig(reconstructed, os.path.join(config.output_dir, f"{config.dataset_name}_{os.path.basename(config.checkpoint_path).removesuffix('.pth')}.png"))
