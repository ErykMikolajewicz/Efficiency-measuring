from time import process_time
import gc

import polars as pl
from tqdm import tqdm
from scipy.stats import mannwhitneyu


def compute_stats(times: pl.Series) -> dict[str, float]:
    stats = {'mean': times.mean(),
             'median': times.median(),
             'max': times.max(),
             'min': times.min(),
             'std': times.std()
             }

    return stats


def measure_times(function, n_iterations, n_loops, *args, **kwargs):
    gc.disable()
    times = pl.zeros(n_iterations, pl.Float64, eager=True)
    for i in tqdm(range(n_iterations)):
        t1 = process_time()
        for _ in range(n_loops):
            function(*args, **kwargs)
        t2 = process_time()
        times[i] = (t2 - t1)
    gc.enable()
    return times


def test_statistic_relevant(previous, post) -> float:
    results = mannwhitneyu(previous, post)
    p_value = results[1]
    return p_value
