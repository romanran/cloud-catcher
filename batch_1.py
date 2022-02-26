from cloud_catcher import CloudCatcher
from datetime import datetime

satellite = 'G16'
target_dir_name = f"W:\\satellite-data\\ABI-{satellite}\\batch-1"
first = CloudCatcher(target_dir_name, satellite)
step_hours = 3
steps = 1 * (24 // step_hours)
first.start(datetime(2022, 1, 31, 14), step_hours, 1)
