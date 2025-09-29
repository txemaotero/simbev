"""
Script to generate power consumption profiles within a date range.
"""

import argparse
import pathlib
import datetime
import pandas as pd
import numpy as np
from simbev.simbev_class import SimBEV

COMPONENT_COLS = [
    "home_detached_total_power",
    "home_apartment_total_power",
    "work_total_power",
    "street_total_power",
    "retail_total_power",
    "urban_fast_total_power",
    "highway_fast_total_power",
]

def aggregate_total_power(grid_time_series_all_regions: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """
    Return
    ------
    np.ndarray: 0 row = timestamp, 1 row aggregation
    """
    timestamps = grid_time_series_all_regions["timestamp"].to_numpy()
    total_power = grid_time_series_all_regions[COMPONENT_COLS].sum(axis=1).to_numpy()
    return timestamps, total_power

def plot_power_components(grid_time_series_all_regions: pd.DataFrame, columns: list[str] | None = None) -> None:
    """
    Plots each power component individually with a legend.
    """
    if columns is None:
        columns = COMPONENT_COLS
    else:
        assert all(c in COMPONENT_COLS for c in columns), "Invalid given column"

    timestamps = grid_time_series_all_regions["timestamp"].to_numpy()

    import matplotlib
    matplotlib.use('Qt5Agg')
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 6))
    for col in columns:
        plt.plot(timestamps, grid_time_series_all_regions[col], label=col)

    plt.xlabel("Timestamp")
    plt.ylabel("Power Consumption (kW)")  # Adjust units if needed
    plt.title("Power Consumption by Category")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("curve.png")
    # plt.show()

def get_date(date_str: str) -> datetime.date:
    return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()


config_path = pathlib.Path("../scenarios/galicia/configs/galicia.cfg").absolute()

meses = [
    ("2023-02", "2023-02-01", "2023-03-01"),
    ("2023-03", "2023-03-01", "2023-04-01"),
    ("2023-04", "2023-04-01", "2023-05-01"),
    ("2023-05", "2023-05-01", "2023-06-01"),
    ("2023-06", "2023-06-01", "2023-07-01"),
    ("2023-07", "2023-07-01", "2023-08-01"),
    ("2023-08", "2023-08-01", "2023-09-01"),
    ("2023-09", "2023-09-01", "2023-10-01"),
    ("2023-10", "2023-10-01", "2023-11-01"),
    ("2023-11", "2023-11-01", "2023-12-01"),
    ("2023-12", "2023-12-01", "2024-01-01"),
]

for fname, start, end in meses:
    print("Simulating", fname)
    simbev, cfg = SimBEV.from_config(config_path)
    simbev.set_start_date(get_date(start))
    simbev.set_end_date(get_date(end))
    simbev.setup()
    simbev.run_multi()
    grid_time_series_all_regions = simbev.get_grid_time_series_all_regions()
    grid_time_series_all_regions.to_csv(fname + ".csv")


# plot_power_components(grid_time_series_all_regions, ["highway_fast_total_power"])
# plot_power_components(grid_time_series_all_regions)
