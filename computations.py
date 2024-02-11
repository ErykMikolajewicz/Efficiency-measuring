from time import time

import polars as pl
from tqdm import tqdm


def compute_stats(times: pl.Series) -> dict[str, float]:
    stats = {'mean': times.mean(),
             'median': times.median(),
             'min': times.min(),
             'max': times.max(),
             'std': times.std()
             }

    return stats


def measure_times(function, n_iterations, n_loops, *args, **kwargs):
    times = pl.zeros(n_iterations, pl.Float64, eager=True)
    for i in tqdm(range(n_iterations)):
        t1 = time()
        for _ in range(n_loops):
            function(*args, **kwargs)
        t2 = time()
        times[i] = (t2 - t1)
    return times
