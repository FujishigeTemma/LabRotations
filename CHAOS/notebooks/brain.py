import os
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
import PIL.Image
import polars as pl
import wandb
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from tinygrad import Tensor
from tinygrad.dtype import dtypes
from tinygrad.engine.jit import TinyJit
from tinygrad.helpers import CI, trange
from tinygrad.nn.optim import Adam
from tinygrad.nn.state import get_parameters

# Initialize Weights & Biases
wandb.init(project="brain-action-prediction", name="transformer-brain-recording")
wandb.config.update({"model": "transformer", "dim": 100, "layers": 2, "embed_dim": 128})
wandb.define_metric("epoch")


def make_dataset_brain():
    data_dir = "../data"

    df = pl.read_csv(os.path.join(data_dir, "motor_brain_run6.csv")).drop("")

    N = len(df.columns) - 4
    X = df[:, -N:].to_numpy()

    X = X[:, np.std(X, axis=0) != 0]
    N = X.shape[1]

    print(X.shape)  # (295, 85265)

    Y = df["Brake", "Acceleration", "Steer"].to_numpy()

    return X[:140, :], Y[:140], X[140:, :], Y[140:]


def make_dataset(dim=100):
    """
    Create a dataset from brain recording data to predict action values.
    Returns training and testing data splits.

    Args:
        dim: Number of brain recording features to use
    """
    X_train, Y_train, X_test, Y_test = make_dataset_brain()

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    pca = PCA(n_components=dim)
    X_train = pca.fit_transform(X_train)
    X_test = pca.transform(X_test)

    return X_train, Y_train, X_test, Y_test


class TransformerBlock:
    def __init__(self, embed_dim, num_heads, ff_dim, prenorm=False, act=lambda x: x.relu(), dropout=0.1):
        assert embed_dim % num_heads == 0, "embed_dim must be divisible by num_heads"

        self.num_heads = num_heads
        self.head_size = embed_dim // num_heads
        self.prenorm, self.act = prenorm, act
        self.dropout = dropout

        self.query = (Tensor.scaled_uniform(embed_dim, embed_dim), Tensor.zeros(embed_dim))
        self.key = (Tensor.scaled_uniform(embed_dim, embed_dim), Tensor.zeros(embed_dim))
        self.value = (Tensor.scaled_uniform(embed_dim, embed_dim), Tensor.zeros(embed_dim))

        self.out = (Tensor.scaled_uniform(embed_dim, embed_dim), Tensor.zeros(embed_dim))

        self.ff1 = (Tensor.scaled_uniform(embed_dim, ff_dim), Tensor.zeros(ff_dim))
        self.ff2 = (Tensor.scaled_uniform(ff_dim, embed_dim), Tensor.zeros(embed_dim))

        self.ln1 = (Tensor.ones(embed_dim), Tensor.zeros(embed_dim))
        self.ln2 = (Tensor.ones(embed_dim), Tensor.zeros(embed_dim))

    def attn(self, x):
        # x: (bs, time, embed_dim) -> (bs, time, embed_dim)
        query, key, value = [
            x.linear(*y).reshape(shape=(x.shape[0], -1, self.num_heads, self.head_size)).transpose(1, 2) for y in [self.query, self.key, self.value]
        ]
        attention = Tensor.scaled_dot_product_attention(query, key, value).transpose(1, 2)
        return attention.reshape(shape=(x.shape[0], -1, self.num_heads * self.head_size)).linear(*self.out)

    def __call__(self, x):
        if self.prenorm:
            x = x + self.attn(x.layernorm().linear(*self.ln1)).dropout(self.dropout)
            x = x + self.act(x.layernorm().linear(*self.ln2).linear(*self.ff1)).linear(*self.ff2).dropout(self.dropout)
        else:
            x = x + self.attn(x).dropout(self.dropout)
            x = x.layernorm().linear(*self.ln1)
            x = x + self.act(x.linear(*self.ff1)).linear(*self.ff2).dropout(self.dropout)
            x = x.layernorm().linear(*self.ln2)
        return x


class Transformer:
    def __init__(self, input_dim, output_dim, layers=2, embed_dim=128, num_heads=4, ff_dim=32):
        self.input_dim, self.output_dim = input_dim, output_dim
        self.embed = Tensor.scaled_uniform(input_dim, embed_dim, requires_grad=False)
        self.tbs = [TransformerBlock(embed_dim, num_heads, ff_dim) for _ in range(layers)]
        self.final = Tensor.scaled_uniform(embed_dim, output_dim)

    def forward(self, x):
        bs = x.shape[0]

        # For brain data, we treat each sample as a single input vector
        # We add a sequence dimension of 1 to make it compatible with the transformer
        x = x.reshape((bs, 1, -1))

        # Process through the model
        x = x.linear(self.embed)  # Project to embedding dimension
        x = x.sequential(self.tbs)  # Process through transformer blocks
        x = x.linear(self.final)  # Project to output dimension
        return x.reshape((bs, -1, x.shape[-1]))


def log_predictions(epoch, X_test, Y_test, Y_pred, num_samples=5):
    """
    Log predictions vs actual values to Weights & Biases
    """
    # Create a figure with subplots for each action (Brake, Acceleration, Steer)
    fig, axes = plt.subplots(3, 1, figsize=(10, 15))
    action_names = ["Brake", "Acceleration", "Steer"]

    # Plot actual vs predicted for each action
    for i, name in enumerate(action_names):
        ax = axes[i]
        ax.plot(Y_test[:num_samples, i], "b-", label="Actual")
        ax.plot(Y_pred[:num_samples, i], "r--", label="Predicted")
        ax.set_title(f"{name} - Actual vs Predicted")
        ax.set_xlabel("Sample")
        ax.set_ylabel("Value")
        ax.legend()

    plt.tight_layout()

    # Save figure to buffer and log to wandb
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    img = PIL.Image.open(buf)
    wandb.log({f"predictions_epoch_{epoch}": wandb.Image(img)})
    plt.close(fig)

    # Create a time series plot for all test samples
    fig, axes = plt.subplots(3, 1, figsize=(15, 10))
    action_names = ["Brake", "Acceleration", "Steer"]

    # Plot time series for each action
    for i, name in enumerate(action_names):
        ax = axes[i]
        ax.plot(Y_test[:, i], "b-", label="Actual", alpha=0.7)
        ax.plot(Y_pred[:, i], "r--", label="Predicted", alpha=0.7)
        ax.set_title(f"{name} - Time Series")
        ax.set_xlabel("Time Step")
        ax.set_ylabel("Value")
        ax.legend()

        # Calculate and display correlation
        correlation = np.corrcoef(Y_test[:, i], Y_pred[:, i])[0, 1]
        ax.text(0.02, 0.95, f"Correlation: {correlation:.4f}", transform=ax.transAxes, bbox=dict(facecolor="white", alpha=0.8))

    plt.tight_layout()
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    img = PIL.Image.open(buf)
    wandb.log({f"time_series_epoch_{epoch}": wandb.Image(img)})
    plt.close(fig)


def batched_correlation(out, y):
    assert y.shape == out.shape, f"shapes must match, got y:{y.shape} and out:{out.shape}"
    assert len(y.shape) == 2, f"input must be a 2D tensor, got shape {y.shape}"

    mean_out = out.mean(axis=0).reshape(1, -1)  # [1, Dim]
    mean_y = y.mean(axis=0).reshape(1, -1)  # [1, Dim]

    centered_out = out - mean_out  # [N, Dim]
    centered_y = y - mean_y  # [N, Dim]

    var_out = (centered_out**2).mean(axis=0).reshape(1, -1)  # [1, Dim]
    var_y = (centered_y**2).mean(axis=0).reshape(1, -1)  # [1, Dim]

    std_out = var_out.sqrt()  # [1, Dim]
    std_y = var_y.sqrt()  # [1, Dim]

    cov = (centered_out * centered_y).mean(axis=0).reshape(1, -1)  # [1, Dim]

    pearson_corr = cov / (std_y * std_out)  # [1, Dim]

    return pearson_corr


def combined_loss_fn(out, y, corr_weight=0.5):
    """
    Combined loss function with MSE and correlation

    Args:
        out: Predicted values tensor
        y: Target values tensor
        corr_weight: Weight for correlation loss component

    Returns:
        Combined loss tensor
    """
    # MSE component
    mse_loss = out.sub(y).pow(2).mean()

    correlation = batched_correlation(out, y)
    corr_loss = (1 - correlation).mean().mul(corr_weight)

    return mse_loss.add(corr_loss)


def train(
    model,
    X_train,
    Y_train,
    optim,
    steps,
    batch_size=128,
    lossfn=lambda out, y: out.sub(y).pow(2).mean(),  # Default to MSE loss
    transform=lambda x: x,
    target_transform=lambda x: x,
    allow_jit=True,
):
    def train_step(x, y):
        # network
        out = model.forward(x) if hasattr(model, "forward") else model(x)
        loss = lossfn(out, y)
        optim.zero_grad()
        loss.backward()
        optim.step()
        # For regression, we use mean absolute error as a metric instead of accuracy
        accuracy = out.reshape(y.shape).sub(y).abs().mean()
        return loss.realize(), accuracy.realize()

    if allow_jit:
        train_step = TinyJit(train_step)

    with Tensor.train():
        losses, accuracies = [], []
        for i in (t := trange(steps, disable=CI)):
            samp = np.random.randint(0, X_train.shape[0], size=(batch_size))
            x = Tensor(transform(X_train[samp]), requires_grad=False, dtype=dtypes.float32)
            y = Tensor(target_transform(Y_train[samp]), dtype=dtypes.float32)
            loss, accuracy = train_step(x, y)

            loss, accuracy = loss.numpy(), accuracy.numpy()
            losses.append(loss)
            accuracies.append(accuracy)

            wandb.log({"train/loss": loss, "train/mae": accuracy, "train/step": i + steps * len(losses)})
            t.set_description(f"loss {loss:.4f} mae {accuracy:.4f}")
    return [losses, accuracies]


def evaluate(model, X_test, Y_test, batch_size=128, return_predict=False, transform=lambda x: x, target_transform=lambda y: y):
    Tensor.training = False

    def numpy_eval(Y_test):
        Y_test_preds = np.zeros_like(Y_test)
        for i in trange((len(Y_test) - 1) // batch_size + 1, disable=CI):
            x = Tensor(transform(X_test[i * batch_size : (i + 1) * batch_size]), dtype=dtypes.float32)
            out = model.forward(x) if hasattr(model, "forward") else model(x)
            Y_test_preds[i * batch_size : (i + 1) * batch_size] = out.reshape((-1, Y_test.shape[1])).numpy()
        Y_test = target_transform(Y_test)

        mae = np.abs(Y_test - Y_test_preds).mean()

        # Calculate mean correlation across all dimensions
        mean_corr = np.mean([np.corrcoef(Y_test[:, i], Y_test_preds[:, i])[0, 1] for i in range(Y_test.shape[1])])

        return mae, mean_corr, Y_test_preds

    mae, mean_corr, Y_test_pred = numpy_eval(Y_test)

    metrics = {"eval/mae": mae, "eval/mean_correlation": mean_corr, "eval/samples": len(Y_test)}
    for i, name in enumerate(["Brake", "Acceleration", "Steer"]):
        metrics[f"eval/correlation_{name}"] = np.corrcoef(Y_test[:, i], Y_test_pred[:, i])[0, 1]
    wandb.log(metrics)
    print(f"Test set mean absolute error: {mae:.6f}")
    return (mae, Y_test_pred) if return_predict else mae


def update_lr_cycle(max_lr, min_lr, step_size, epoch):
    cycle = np.floor(1 + epoch / (2 * step_size))
    x = np.abs(epoch / step_size - 2 * cycle + 1)
    lr = min_lr + (max_lr - min_lr) * np.maximum(0, (1 - x))
    return lr


def update_lr_expotential(max_lr, min_lr, decay_rate, epoch):
    lr = min_lr + (max_lr - min_lr) * np.exp(-decay_rate * epoch)
    return lr


if __name__ == "__main__":
    X_train, Y_train, X_test, Y_test = make_dataset(dim=100)  # Use 100 brain recording features
    input_dim = X_train.shape[1]  # Number of brain recording features
    output_dim = Y_train.shape[1]  # Number of action values (Brake, Acceleration, Steer)
    wandb.config.update({"input_dim": input_dim, "output_dim": output_dim})
    model = Transformer(input_dim=input_dim, output_dim=output_dim)

    # Print shapes to verify
    print(f"Training data shapes: X={X_train.shape}, Y={Y_train.shape}")
    print(f"Testing data shapes: X={X_test.shape}, Y={Y_test.shape}")

    batch_size = 64
    max_epochs = 100
    lr = 2e-3
    max_lr = 2e-3
    min_lr = 1e-7
    corr_weight = 0.5  # Weight for correlation loss
    all_metrics = {"epoch": [], "mae": [], "correlation": [], "lr": []}

    for i in range(max_epochs):
        optim = Adam(get_parameters(model), lr=lr)
        print(f"\nEpoch {i + 1}/{max_epochs}:")
        train(
            model,
            X_train,
            Y_train,
            optim,
            50,
            batch_size=batch_size,
            lossfn=lambda out, y: combined_loss_fn(out, y, corr_weight=corr_weight),
            allow_jit=True,
        )
        mae, mean_corr, Y_test_preds = evaluate(model, X_test, Y_test, return_predict=True)

        # Log predictions vs actual values
        log_predictions(i, X_test, Y_test, Y_test_preds)

        # Track metrics for summary chart
        all_metrics["epoch"].append(i)
        all_metrics["mae"].append(mae)
        all_metrics["correlation"].append(mean_corr)
        all_metrics["lr"].append(lr)

        # lr = update_lr_cycle(max_lr, min_lr, max_epochs * 2 // batch_size, i)
        lr = update_lr_expotential(max_lr, min_lr, 0.05, i)

        # Log epoch-level metrics
        wandb.log({"epoch": i, "eval/epoch_mae": mae, "lr": lr})

        print(f"reducing lr to {lr:.8f}")

    # Print some example predictions
    print("\nExample predictions (first 5 samples):")
    for i in range(min(5, len(Y_test))):
        print(f"Sample {i}:")
        print(f"  Actual: Brake={Y_test[i][0]:.4f}, Acceleration={Y_test[i][1]:.4f}, Steer={Y_test[i][2]:.4f}")
        print(f"  Predicted: Brake={Y_test_preds[i][0]:.4f}, Acceleration={Y_test_preds[i][1]:.4f}, Steer={Y_test_preds[i][2]:.4f}")

    print(f"\nFinal mean absolute error: {mae:.4f}")
    print(f"Final mean correlation: {mean_corr:.4f}")

    # Create a summary chart of training progress
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot MAE
    color = "tab:blue"
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Mean Absolute Error", color=color)
    ax1.plot(all_metrics["epoch"], all_metrics["mae"], "o-", color=color)
    ax1.tick_params(axis="y", labelcolor=color)
    ax1.set_title("Training Progress: MAE, Correlation, and Learning Rate")

    # Add learning rate on secondary y-axis
    ax2 = ax1.twinx()
    color = "tab:red"
    ax2.set_ylabel("Learning Rate", color=color)
    ax2.plot(all_metrics["epoch"], all_metrics["lr"], "o-", color=color)
    ax2.tick_params(axis="y", labelcolor=color)

    # Add correlation on a third y-axis
    ax3 = ax1.twinx()
    ax3.spines["right"].set_position(("outward", 60))  # Offset the third y-axis
    color = "tab:green"
    ax3.set_ylabel("Mean Correlation", color=color)
    ax3.plot(all_metrics["epoch"], all_metrics["correlation"], "o-", color=color)
    ax3.tick_params(axis="y", labelcolor=color)

    # Log the summary chart
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    img = PIL.Image.open(buf)
    wandb.log({"training_summary": wandb.Image(img)})
    plt.close(fig)

    # Finish wandb run
    wandb.finish()
