import time
import signal
from multi_catch import multi_catch
from datetime import datetime, timedelta
import multiprocessing
multiprocessing.freeze_support()

satellite = 'G16'

config = {
    'target_dir': f"W:\\satellite-data\\ABI-{satellite}\\batch-1",
    'data_save_dir': "W:\\satellite-data\\data",
    'satellite': satellite,
    'start_date': datetime(2022, 2, 2, 20),
    'every_nth_hour': 3,
    'days': 2,
    'dpi': 900
}


multi_catch(**config)
