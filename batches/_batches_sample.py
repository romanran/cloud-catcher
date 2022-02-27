from datetime import datetime

batches = {
    'batch-1': {
        'satellite': 'G16',
        'target_dir': "C:\\data\\ABI-G16\\batch-1",
        'data_save_dir': "C:\\data\\data",
        'start_date': datetime(2022, 1, 31, 20),
        'every_nth_hour': 3,
        'days': 7,
        'dpi': 900,
        'band': 16  # 1-16 https://www.goes-r.gov/mission/ABI-bands-quick-info.html
    }
}
