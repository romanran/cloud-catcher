from datetime import datetime

batches = {
    'batch-1': {
        'satellite': 'G16',
        'target_dir': "C:\\data\\ABI-G16\\batch-1",
        'data_save_dir': "C:\\data\\data",
        'start_date': datetime(2022, 1, 31, 20),
        'every_nth_hour': 3,
        'days': 28,
        'dpi': 900
    }
}
