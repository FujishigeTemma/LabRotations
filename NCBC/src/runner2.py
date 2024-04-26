import concurrent.futures
import os

from analysis import analyze
from recorders.db import DB
from tqdm import tqdm

output = "../outputs"


def run_analysis():
    total_simulations = len(range(100, 1100, 100)) * len(range(10, 70, 10)) * 2 * len(range(10, 110, 10))

    with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
        futures = []
        with DB(os.path.join(output, "ring.sqlite")) as db:
            jobs = db.list("jobs")
        for job in jobs:
            future = executor.submit(
                analyze,
                output=output,
                job_id=job[0],
            )
            futures.append(future)

        with tqdm(total=total_simulations, unit="simulation") as progress_bar:
            for future in concurrent.futures.as_completed(futures):
                progress_bar.update(1)

        concurrent.futures.wait(futures)

    return


if __name__ == "__main__":
    run_analysis()
