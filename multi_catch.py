import numpy as np
import time
import signal
from cloud_catcher import CloudCatcher
from datetime import datetime, timedelta
import multiprocessing
multiprocessing.freeze_support()

satellite = 'G16'

jobs = []


def multi_catch(target_dir, data_save_dir, satellite, start_date, every_nth_hour, days, dpi=900):
    no_of_photos = days * (24 // every_nth_hour)

    def main_task(step_index, start_date):
        date = start_date + timedelta(hours=every_nth_hour * step_index)
        first = CloudCatcher(target_dir, data_save_dir, satellite, dpi)
        first.start(date)

    with multiprocessing.Pool(multiprocessing.cpu_count()) as process_pool:
        try:
            process_pool.map(
                main_task, [(step_index, start_date, target_dir, data_save_dir, satellite, dpi) for step_index in range(no_of_photos)])
            process_pool.join()
            jobs.append(process_pool)
            process_pool.close()
        except KeyboardInterrupt:
            print("Caught KeyboardInterrupt, terminating workers")
            process_pool.terminate()
        else:
            print("Normal termination")
            process_pool.close()
        process_pool.join()
