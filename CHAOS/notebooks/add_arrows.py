import generate
import numpy as np
import plotly.graph_objects as go
from edmkit.simplex_projection import pairwise_distance, topk
from tinygrad import Tensor
from tinygrad.dtype import dtypes

# Parameters from the notebook
sigma, rho, beta = 10, 28, 8 / 3
dt = 0.01
t_max = 100
X0 = np.array([0.1, 0.0, 0.0])

# Generate Lorenz attractor data
r, x = generate.lorenz(sigma, rho, beta, X0, dt, t_max)

# Convert to Tensor
x_tensor = Tensor(x, dtype=dtypes.float32)

# Parameters for finding nearest neighbors
index = 278
k = 3
exclusion_radius = 2

# Calculate pairwise distances
D = pairwise_distance(x_tensor).numpy()
N = D.shape[0]
mask = np.ones(N, dtype=bool)
mask[index] = False
mask[max(0, index - exclusion_radius) : min(N, index + exclusion_radius + 1)] = False

# Find k-nearest neighbors
indices_masked, _ = topk(D[index][mask], k, largest=False)
indices = np.arange(N)[mask][indices_masked]

# Convert back to numpy for plotting
x = x_tensor.numpy()

# Create layout
layout = go.Layout(
    scene=dict(xaxis=dict(title="X"), yaxis=dict(title="Y"), zaxis=dict(title="Z")),
    width=800,
    height=800,
)

# Create data traces
data = [
    go.Scatter3d(
        name="lorenz",
        x=x[:, 0],
        y=x[:, 1],
        z=x[:, 2],
        mode="markers",
        marker=dict(size=2),
    ),
    go.Scatter3d(
        name="knn",
        x=x[indices][:, 0],
        y=x[indices][:, 1],
        z=x[indices][:, 2],
        mode="markers",
        marker=dict(size=5, color="red"),
    ),
    go.Scatter3d(
        name="target",
        x=[x[index][0]],
        y=[x[index][1]],
        z=[x[index][2]],
        mode="markers",
        marker=dict(size=5, color="green"),
    ),
    go.Scatter3d(
        name="shifted",
        x=x[indices + 3][:, 0],
        y=x[indices + 3][:, 1],
        z=x[indices + 3][:, 2],
        mode="markers",
        marker=dict(size=5, color="pink"),
    ),
    go.Scatter3d(
        name="predicted",
        x=[np.sum(x[indices + 3][:, 0]) / k],
        y=[np.sum(x[indices + 3][:, 1]) / k],
        z=[np.sum(x[indices + 3][:, 2]) / k],
        mode="markers",
        marker=dict(size=5, color="purple"),
    ),
]

# Add arrows from each knn point to its corresponding shifted point
for i in range(len(indices)):
    # Create arrow from knn to shifted
    arrow = go.Scatter3d(
        x=[x[indices[i]][0], x[indices[i] + 3][0]],
        y=[x[indices[i]][1], x[indices[i] + 3][1]],
        z=[x[indices[i]][2], x[indices[i] + 3][2]],
        mode="lines",
        line=dict(color="yellow", width=5),
        showlegend=False if i > 0 else True,
        name="knn→shifted" if i == 0 else None,
        opacity=0.8,
    )

    # Add the arrow to the data
    data.append(arrow)

# Create and show figure
fig = go.Figure(data=data, layout=layout)
fig.show()
