import math

import numpy as np
import plotly.graph_objects as go
import polars as pl
import pyEDM
from matplotlib import colormaps
from PIL import Image
from plotly.subplots import make_subplots


def autocorrelation(x: pl.Series, max_lag: int):
    lags = range(max_lag)
    autocorr = [1] + [np.corrcoef(x[:-lag], x[lag:])[0, 1] for lag in lags[1:]]
    return np.array(autocorr)


def plot_timeseries(df: pl.DataFrame):
    t = list(range(len(df)))

    layout = go.Layout(
        title="Time Series",
        xaxis=dict(title="t"),
        yaxis=dict(title="Expression"),
    )

    data = [go.Scatter(x=t, y=df[column], name=column, showlegend=False) for column in df.columns]

    fig = go.Figure(data=data, layout=layout)
    fig.show()


def plot_distributions(df1: pl.DataFrame, df2: pl.DataFrame):
    mean1 = np.log(df1.mean()).squeeze()
    mean2 = np.log(df2.mean()).squeeze()

    layout = go.Layout(
        title="Expression level distribution",
        xaxis=dict(title="expression level"),
        yaxis=dict(title="frequency"),
        # barmode="overlay",
    )

    data = [
        go.Histogram(x=mean1, name="1st half", opacity=0.5),
        go.Histogram(x=mean2, name="2nd half", opacity=0.5),
    ]

    fig = go.Figure(data=data, layout=layout)
    fig.show()


def plot_columns(df: pl.DataFrame, columns: list[str]) -> None:
    fig = make_subplots(
        rows=math.ceil(len(columns) / 3),
        cols=3 if len(columns) >= 3 else len(columns),
        subplot_titles=columns,
        shared_yaxes=True,
        horizontal_spacing=0.01,
        vertical_spacing=0.3 / math.ceil(len(columns) / 3),
    )

    for i, column in enumerate(columns):
        # sampling interval is 5 minutes
        fig.add_trace(
            go.Scatter(x=[v * 5 for v in range(df.shape[0])], y=df[column], name=column),
            row=i // 3 + 1,
            col=i % 3 + 1,
        )
        if i % 3 == 0:
            fig.update_yaxes(title_text="Expression", row=i // 3 + 1, col=1)
        # if last row, update x-axis title
        if i >= len(columns) - 3:
            fig.update_xaxes(title_text="time (min)", row=i // 3 + 1, col=i % 3 + 1)

    fig.update_layout(height=300 * math.ceil(len(columns) / 3), width=1000, showlegend=False)
    fig.show()


def plot_embedding2D(df: pl.DataFrame, columns: list[str]) -> None:
    assert len(columns) == 2
    layout = go.Layout(
        title="2D Embedding Plot",
        xaxis_title=columns[0],
        yaxis_title=columns[1],
        width=500,
        height=400,
    )
    data = go.Scatter(x=df[columns[0]], y=df[columns[1]], mode="lines")

    fig = go.Figure(data=data, layout=layout)
    fig.show()


def plot_embedding3D(df: pl.DataFrame, columns: list[str], eye: dict) -> None:
    assert len(columns) == 3
    layout = go.Layout(
        title="3D Embedding Plot",
        scene=dict(
            xaxis_title=columns[0],
            yaxis_title=columns[1],
            zaxis_title=columns[2],
            camera=dict(eye=eye),
        ),
        width=600,
        height=600,
    )
    data = go.Scatter3d(
        x=df[columns[0]],
        y=df[columns[1]],
        z=df[columns[2]],
        mode="lines",
        hovertemplate=f"{columns[0]}: %{{x}}<br>{columns[1]}: %{{y}}<br>{columns[2]}: %{{z}}",
    )

    fig = go.Figure(data=data, layout=layout)
    fig.show()


def plot_embedding4D(df: pl.DataFrame, columns: list[str], eye: dict) -> None:
    assert len(columns) == 4
    layout = go.Layout(
        title="4D Embedding Plot",
        scene=dict(
            xaxis_title=columns[0],
            yaxis_title=columns[1],
            zaxis_title=columns[2],
            camera=dict(eye=eye),
        ),
        width=600,
        height=600,
    )
    data = go.Scatter3d(
        x=df[columns[0]],
        y=df[columns[1]],
        z=df[columns[2]],
        mode="lines",
        line=dict(color=df[columns[3]], colorscale="Viridis"),
        hovertemplate=f"{columns[0]}: %{{x}}<br>{columns[1]}: %{{y}}<br>{columns[2]}: %{{z}}<br>{columns[3]}: %{{line.color}}",
    )

    fig = go.Figure(data=data, layout=layout)
    fig.show()


def plot_rho_Tp_tau(df: pl.DataFrame, columns: list[str], E: int, maxTp: int, minTau: int):
    PredictIntervalKwargs = {
        "dataFrame": df.to_pandas(),
        "lib": [1, df.shape[0] // 2],
        "pred": [df.shape[0] // 2 + 1, df.shape[0]],
        "maxTp": maxTp,
        "E": E,
        "showPlot": False,
    }

    tau_range = range(-1, minTau - 1, -1)
    Tp_range = range(1, maxTp + 1)

    fig = make_subplots(
        rows=1,
        cols=len(columns),
        subplot_titles=columns,
        horizontal_spacing=0.01,
        specs=[[{"type": "surface"} for _ in range(len(columns))]],
    )

    for i, column in enumerate(columns):
        rho = []
        for tau in tau_range:
            result = pyEDM.PredictInterval(columns=column, target=column, tau=tau, **PredictIntervalKwargs)
            rho.append(result["rho"].values)

        Tp, tau = np.meshgrid(Tp_range, tau_range)
        rho = np.array(rho)

        autocorr = autocorrelation(df[column], max_lag=maxTp)
        autocorr = np.repeat(autocorr.reshape(1, -1), len(tau_range), axis=0)

        fig.add_trace(
            go.Surface(x=Tp, y=tau, z=rho, scene=f"scene{i+1}", showscale=False),
            row=1,
            col=i + 1,
        )
        fig.add_trace(
            go.Surface(
                x=Tp,
                y=tau,
                z=autocorr,
                opacity=0.5,
                showscale=False,
                scene=f"scene{i+1}",
            ),
            row=1,
            col=i + 1,
        )

    fig.update_scenes(
        xaxis_title_text="Tp",
        yaxis_title_text="tau",
        zaxis_title_text="rho",
        zaxis_range=[-1, 1],
    )

    fig.update_layout(height=400, width=len(columns) * 400, margin=dict(l=20, r=20, t=30, b=30))
    fig.show()


def plot_rho_Tp(df: pl.DataFrame, columns: list[str], E: int, maxTp: int, tau: int):
    PredictIntervalKwargs = {
        "dataFrame": df.to_pandas(),
        "lib": [1, df.shape[0] // 2],
        "pred": [df.shape[0] // 2 + 1, df.shape[0]],
        "maxTp": maxTp,
        "E": E,
        "tau": tau,
        "showPlot": False,
    }

    Tp = list(range(1, maxTp + 1))

    fig = make_subplots(
        rows=len(columns),
        cols=1,
        subplot_titles=columns,
        shared_xaxes=True,
        vertical_spacing=0.05,
    )

    for i, column in enumerate(columns):
        rho = pyEDM.PredictInterval(columns=column, target=column, **PredictIntervalKwargs)["rho"]
        autocorr = autocorrelation(df[column], max_lag=maxTp)

        showlegend = True if i == 0 else False

        fig.add_trace(
            go.Scatter(
                x=Tp,
                y=rho,
                name="rho",
                line=dict(color="red"),
                showlegend=showlegend,
            ),
            row=i + 1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=Tp,
                y=autocorr,
                name="Autocorrelation",
                line=dict(color="blue"),
                showlegend=showlegend,
            ),
            row=i + 1,
            col=1,
        )

    fig.update_xaxes(title_text="Tp", row=len(columns), col=1)
    fig.update_yaxes(title_text="rho")

    fig.update_layout(
        width=800,
        height=200 * len(columns),
        margin=dict(l=20, r=20, t=30, b=30),
        hoversubplots="axis",
        hovermode="x",
    )

    fig.show()


def plot_rho_E_tau(df: pl.DataFrame, columns: list[str], maxE: int, Tp: int, minTau: int):
    EmbedDimensionKwargs = {
        "dataFrame": df.to_pandas(),
        "lib": [1, df.shape[0] // 2],
        "pred": [df.shape[0] // 2 + 1, df.shape[0]],
        "maxE": maxE,
        "Tp": Tp,
        "showPlot": False,
    }

    tau_range = range(-1, minTau - 1, -1)
    E_range = range(1, maxE + 1)

    fig = make_subplots(
        rows=1,
        cols=len(columns),
        subplot_titles=columns,
        horizontal_spacing=0.01,
        specs=[[{"type": "surface"} for _ in range(len(columns))]],
    )

    for i, column in enumerate(columns):
        rho = []
        for tau in tau_range:
            result = pyEDM.EmbedDimension(columns=column, target=column, tau=tau, **EmbedDimensionKwargs)
            rho.append(result["rho"].values)

        E, tau = np.meshgrid(E_range, tau_range)
        rho = np.array(rho)

        fig.add_trace(
            go.Surface(
                x=E,
                y=tau,
                z=rho,
                scene=f"scene{i+1}",
                showscale=False,
                hovertemplate="E: %{x}<br>tau: %{y}<br>rho: %{z}",
            ),
            row=1,
            col=i + 1,
        )

    fig.update_scenes(
        xaxis_title_text="E",
        yaxis_title_text="tau",
        zaxis_title_text="rho",
        zaxis_range=[-1, 1],
    )

    fig.update_layout(height=400, width=len(columns) * 400, margin=dict(l=20, r=20, t=30, b=30))
    fig.show()


def plot_CCM(df: pl.DataFrame, pairs: list[tuple[str, str]], E: int, Tp: int, tau: int):
    CCMKwargs = {
        "dataFrame": df.to_pandas(),
        "libSizes": [df.shape[0] // 10, df.shape[0] - 10, 5],
        "sample": 10,
        "E": E,
        "Tp": Tp,
        "tau": tau,
        "showPlot": False,
    }

    fig = make_subplots(
        rows=1,
        cols=len(pairs),
        subplot_titles=[f"{pair[0]},{pair[1]}" for pair in pairs],
        shared_yaxes=True,
    )

    for i, pair in enumerate(pairs):
        result = pyEDM.CCM(columns=pair[0], target=pair[1], **CCMKwargs)

        for line in result.columns[1:]:  # type: ignore
            fig.add_trace(
                go.Scatter(x=result["LibSize"], y=result[line], name=line),  # type: ignore
                row=1,
                col=i + 1,
            )
            fig.update_xaxes(title_text="LibSize", row=1, col=i + 1)

    fig.update_layout(
        yaxis_title="rho",
        height=400,
        width=1000,
    )

    fig.show()


def plot_lagged3D(df: pl.DataFrame, column: str, tau: int) -> None:
    col = df[column].to_numpy()

    layout = go.Layout(
        title=f"Lagged Plot for {column}",
        scene=dict(xaxis_title="X(t)", yaxis_title=f"X(t-{tau})", zaxis_title=f"X(t-2*{tau}"),
        width=800,
        height=600,
    )

    data = go.Scatter3d(
        x=col[: -2 * tau],
        y=col[tau:-tau],
        z=col[2 * tau :],
        mode="lines",
        line=dict(width=1),
        hovertemplate=f"X(t): %{{x}}<br>X(t-{tau}): %{{y}}<br>X(t-2*{tau}): %{{z}}<extra></extra>",
    )

    fig = go.Figure(data=data, layout=layout)
    fig.show()


def find_best_E_tau_Tp(df: pl.DataFrame, column: str, maxE: int, minTau: int, maxTp: int):
    SimplexKwargs = {
        "dataFrame": df.to_pandas(),
        "lib": [1, df.shape[0] // 2],
        "pred": [df.shape[0] // 2 + 1, df.shape[0]],
        "columns": column,
        "target": column,
        "showPlot": False,
    }

    rho = np.zeros((maxE, -minTau, maxTp))

    for E in range(1, maxE + 1):
        for tau in range(-1, minTau - 1, -1):
            for Tp in range(1, maxTp + 1):
                result = pyEDM.Simplex(E=E, Tp=Tp, tau=tau, **SimplexKwargs)
                error = pyEDM.ComputeError(
                    result["Observations"],  # type: ignore
                    result["Predictions"],  # type: ignore
                )

                rho[E - 1, -tau - 1, Tp - 1] = error["rho"]

    autocorr = autocorrelation(df[column], maxTp)
    rho -= autocorr

    best_E = np.unravel_index(np.argmax(rho), rho.shape)[0] + 1
    best_Tp = np.unravel_index(np.argmax(rho), rho.shape)[1] + 1
    best_tau = -np.unravel_index(np.argmax(rho), rho.shape)[2] - 1

    return best_E, best_Tp, best_tau, rho


def plot_rho_3D(rho: np.ndarray):
    layout = go.Layout(
        scene=dict(
            xaxis=dict(title="E"),
            yaxis=dict(title="Tp"),
            zaxis=dict(title="tau"),
        )
    )

    X, Y, Z = np.meshgrid(
        np.arange(1, rho.shape[0] + 1),
        np.arange(1, rho.shape[1] + 1),
        np.arange(-1, -rho.shape[2] - 1, -1),
    )

    data = [
        go.Scatter3d(
            x=X.flatten(),
            y=Y.flatten(),
            z=Z.flatten(),
            mode="markers",
            marker=dict(
                size=5,
                color=rho.flatten(),
                colorscale="Viridis",
                colorbar=dict(title="rho"),
                opacity=0.8,
            ),
            hovertemplate="E: %{x}<br>Tp: %{y}<br>tau: %{z}<br>rho: %{marker.color:.3f}<extra></extra>",
        )
    ]

    fig = go.Figure(data=data, layout=layout)
    fig.show()


def find_additional_factors(df: pl.DataFrame, columns: list[str], target: str, Tp: int, tau: int):
    SimplexKwargs = {
        "dataFrame": df.to_pandas(),
        "target": target,
        "lib": [1, df.shape[0] // 2],
        "pred": [df.shape[0] // 2 + 1, df.shape[0]],
        "Tp": Tp,
        "tau": tau,
        "exclusionRadius": len(columns),
        "embedded": True,
        "showPlot": False,
    }

    predictions = dict()
    rhos = []

    result = pyEDM.Simplex(
        columns=columns,  # type: ignore
        E=len(columns),
        **SimplexKwargs,
    )
    predictions["Base"] = result["Predictions"].values[Tp:-Tp]  # type: ignore

    error = pyEDM.ComputeError(result["Observations"], result["Predictions"])  # type: ignore
    rhos.append(("Base", error["rho"]))

    for additional_column in df.columns:
        if additional_column not in columns:
            cols = columns + [additional_column]
            result = pyEDM.Simplex(
                columns=cols,  # type: ignore
                E=0,
                **SimplexKwargs,
            )
            predictions[additional_column] = result["Predictions"].values[Tp:-Tp]  # type: ignore

            error = pyEDM.ComputeError(result["Observations"], result["Predictions"])  # type: ignore
            rhos.append((additional_column, error["rho"]))

    predictions = pl.DataFrame(predictions)
    rhos = pl.DataFrame(rhos, schema={"column": pl.String, "rho": pl.Float64})

    return predictions, rhos


def plot_rho_with_additional_factors(results: pl.DataFrame):
    results = results.sort(by="rho")

    fig = go.Figure(data=go.Scatter(x=list(range(len(results))), y=results["rho"], mode="lines+markers"))

    base_rho = results.row(by_predicate=(pl.col("column") == "Base"))[1]
    fig.add_shape(
        type="line",
        x0=0,
        y0=base_rho,
        x1=len(results) - 1,
        y1=base_rho,
        line=dict(color="red", dash="dash"),
    )

    fig.update_layout(
        title="Additional Factors Performance",
        xaxis_title="Base + Additional Gene",
        yaxis_title="Rho",
    )
    fig.update_xaxes(showticklabels=False)

    fig.show()


def plot_improved_predictions(
    df: pl.DataFrame,
    target: str,
    predictions: pl.DataFrame,
    results: pl.DataFrame,
    k: int,
):
    top_k_result = results.sort(by="rho", descending=True).head(k)

    fig = make_subplots(
        rows=math.ceil(k / 3),
        cols=3,
        subplot_titles=["Base"] + top_k_result["column"].to_list(),
        shared_xaxes=True,
        shared_yaxes=True,
        horizontal_spacing=0.02,
        vertical_spacing=0.02,
    )

    t = list(range(len(df)))

    for i, column in enumerate(["Base"] + top_k_result["column"].to_list()):
        fig.add_trace(
            go.Scatter(
                name="Actual",
                x=t,
                y=df[target],
                mode="lines",
                line=dict(color="blue"),
                showlegend=False,
            ),
            row=i // 3 + 1,
            col=i % 3 + 1,
        )
        fig.add_trace(
            go.Scatter(
                name="Prediction",
                x=t[-len(predictions) :],
                y=predictions[column],
                mode="lines",
                line=dict(color="red", dash="dot"),
                showlegend=False,
            ),
            row=i // 3 + 1,
            col=i % 3 + 1,
        )

    fig.update_layout(
        title=f"Base + {k} additional factors",
        height=300 * math.ceil(k / 3),
    )

    fig.show()


def save_matrix(Matrix: np.ndarray, filename: str, cell_size: int = 1):
    Matrix = (Matrix + 1) / 2

    colormap = colormaps.get_cmap("jet")
    colors = (colormap(Matrix) * 255).astype(np.uint8)
    img = Image.fromarray(colors)

    width, height = img.size
    img = img.resize((width * cell_size, height * cell_size), resample=Image.Resampling.NEAREST)

    img.save(filename)


def plot_rho_curve(arr: np.ndarray):
    generator = np.random.default_rng(42)
    small = len(arr) < 2000
    sorted = np.sort(arr if small else generator.choice(arr, 2000))

    layout = go.Layout(
        title="Rho Curve" if small else f"Rho Curve (Sampled 2000 from {len(arr)})",
        xaxis=dict(title="pair"),
        yaxis=dict(title="rho"),
        width=800,
        height=800,
    )

    data = [
        go.Scatter(
            x=np.arange(len(sorted)),
            y=sorted,
            showlegend=False,
        )
    ]

    fig = go.Figure(data=data, layout=layout)
    fig.show()
