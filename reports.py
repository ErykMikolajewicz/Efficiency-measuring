from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Report:
    function_module: str
    function_name: str
    n_iterations: int
    n_loops: int
    mean: float
    median: float
    max_: float
    min_: float
    std: float
    measurement_date: datetime


