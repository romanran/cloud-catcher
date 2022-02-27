from cloud_catcher.cloud_catcher import CloudCatcher
from datetime import timedelta
import multiprocessing
multiprocessing.freeze_support()
# ------------ STEP 1.1: skip to line 7 for the main task


def main_task(args):
    step_index, config = args
    date = config.get('start_date') + \
        timedelta(hours=config.get('every_nth_hour') * step_index)
    cc = CloudCatcher(config['target_dir'], config['data_save_dir'], config['satellite'], config['dpi'], config['band'], config['cmap'])
    result = cc.start(date)  # to STEP 2!
    del cc
    return result


def multi_catch(config):
    no_of_photos = config.get('days') * (24 // config.get('every_nth_hour'))
    cpus = min(4, multiprocessing.cpu_count() - 1)
    with multiprocessing.Pool(cpus) as process_pool:
        try:
            main_task_args = [(step_index, config)
                              for step_index in range(no_of_photos)]
            tasks = process_pool.map(main_task, main_task_args)
            process_pool.close()
        except KeyboardInterrupt:
            print("Caught KeyboardInterrupt, terminating workers")
            process_pool.terminate()
        else:
            process_pool.close()
        process_pool.join()
    print('\n'.join(str(task) for task in tasks))
    return process_pool
