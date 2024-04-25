import concurrent.futures

from ring import _simulate_ring
from tqdm import tqdm
from typeid import TypeID


def run_simulations():
    total_simulations = len(range(100, 1100, 100)) * len(range(10, 70, 10)) * 2 * len(range(10, 110, 10))

    with concurrent.futures.ProcessPoolExecutor(max_workers=120) as executor:
        futures = []
        for gap_junction in [False, True]:
            for n_cells in range(0, 1100, 100):
                for connectivity in range(10, 70, 10):
                    for frequency in range(10, 110, 10):
                        future = executor.submit(
                            _simulate_ring,
                            job_id=TypeID(prefix="job"),
                            seed=0,
                            n_cells=n_cells,
                            connectivity=connectivity / 100,
                            with_gap_junctions=gap_junction,
                            stimuli="homogeneous_poisson_process",
                            frequency=frequency,
                            output="/flash/KazuU/Temma/outputs",
                        )
                        futures.append(future)

        with tqdm(total=total_simulations, unit="simulation") as progress_bar:
            for future in concurrent.futures.as_completed(futures):
                progress_bar.update(1)

        concurrent.futures.wait(futures)

    return


if __name__ == "__main__":
    run_simulations()
