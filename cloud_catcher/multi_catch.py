from cloud_catcher.cloud_catcher import CloudCatcher
from datetime import timedelta
import multiprocessing
multiprocessing.freeze_support()


def main_task(args):
    step_index, config = args
    date = config.get('start_date') + \
        timedelta(hours=config.get('every_nth_hour') * step_index)
    cc = CloudCatcher(config.get('target_dir'), config.get(
        'data_save_dir'), config.get('satellite'), config.get('dpi'))
    cc.start(date)


def multi_catch(config):
    no_of_photos = config.get('days') * (24 // config.get('every_nth_hour'))

    with multiprocessing.Pool(multiprocessing.cpu_count() - 1) as process_pool:
        try:
            main_task_args = [(step_index, config)
                              for step_index in range(no_of_photos)]
            process_pool.map(main_task, main_task_args)
            process_pool.close()
            print('MULTI CATCH DONE')
        except KeyboardInterrupt:
            print("Caught KeyboardInterrupt, terminating workers")
            process_pool.terminate()
        else:
            process_pool.close()
        process_pool.join()
    return process_pool
