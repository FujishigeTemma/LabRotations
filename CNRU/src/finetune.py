import click
import timm
import torch
from torchinfo import summary


@click.command()
def finetune():
    model = timm.create_model("mobilenetv3_small_100", pretrained=True, num_classes=0)

    with torch.no_grad():
        model.eval()

        # data_config = timm.data.resolve_data_config(model)
        # transforms = timm.data.create_transform(**data_config, is_training=False)

    summary(model, input_size=(16, 3, 28, 28))
