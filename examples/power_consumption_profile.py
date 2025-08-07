"""
Script to generate power consumption profiles within a date range.
"""

import argparse
import pathlib
import datetime
import pandas as pd
import numpy as np
from simbev.simbev_class import SimBEV

def aggregate_total_power(grid_time_series_all_regions: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """
    Return
    ------
    np.ndarray: 0 row = timestamp, 1 row aggregation
    """
    cols = [
        "home_detached_total_power",
        "home_apartment_total_power",
        "work_total_power",
        "street_total_power",
        "retail_total_power",
        "urban_fast_total_power",
        "highway_fast_total_power",
    ]
    timestamps = grid_time_series_all_regions["timestamp"].to_numpy()
    total_power = grid_time_series_all_regions[cols].sum(axis=1).to_numpy()
    return timestamps, total_power

parser = argparse.ArgumentParser(
    description="Run simbev in a given date range and return the power consumption profile"
)
parser.add_argument(
    "config_path",
    help="Set the config path.",
)

parser.add_argument(
    "-b",
    "--begin",
    type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d').date(),
    help="First day to compute consumption. Format: YYYY-mm-dd",
    dest="start_date"
)

parser.add_argument(
    "-e",
    "--end",
    type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d').date(),
    help="Last day to compute consumption. Format: YYYY-mm-dd",
    dest="end_date"
)

p_args = parser.parse_args()
config_path = pathlib.Path(p_args.config_path).absolute()

simbev, cfg = SimBEV.from_config(config_path)

simbev.set_start_date(p_args.start_date)
simbev.set_end_date(p_args.end_date)
simbev.setup()
simbev.run_multi()
grid_time_series_all_regions = simbev.get_grid_time_series_all_regions()

timestamps, power = aggregate_total_power(grid_time_series_all_regions)

import matplotlib
matplotlib.use('Qt5Agg')

import matplotlib.pyplot as plt
plt.plot(timestamps, power)
plt.show()
