import os
from goes2go.data import  goes_nearesttime
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class CloudCatcher: 
    def __init__(self, dir, satellite):
        self.dir = dir
        self.satellite = satellite
        self.__ensure_dir()

    def __ensure_dir(self,):
        if not os.path.exists(self.dir): 
            os.makedirs(self.dir)

    def __save_image(self, target_dir_name, photo_name, photo):
        target_path = os.path.join(target_dir_name, f"{photo_name}.png").replace("\\","/")
        print('SAVING TO: ',target_path)
        ax = plt.subplot(projection=photo.rgb.crs)
        ax.imshow(photo.rgb.NaturalColor(gamma=1, pseudoGreen=True, night_IR=True), **photo.rgb.imshow_kwargs)
        ax.coastlines()
        ax.set_facecolor('black')

        plt.tight_layout()
        plt.axis('off')
        plt.subplots_adjust(wspace=0.01)
        plt.savefig(target_path, dpi=300, bbox_inches='tight')

    def start(self, start_date, step_hours, no_of_photos):
        for x in range(no_of_photos):
            shot_date = start_date + timedelta(hours=step_hours * x)
            photo_name = shot_date.strftime("%Y_%m_%d-%H")
            print(photo_name)
            photo = self.__get_photo_from(shot_date)
            self.__save_image(target_dir_name, photo_name, photo)

    def __get_photo_from(self, shot_date):
        return goes_nearesttime(shot_date,
            satellite=self.satellite,
            product='ABI',
            overwrite=False,
            domain='F',
            return_as='xarray')

satellite = 'G16'
target_dir_name = f"W:\\satellite-data\\ABI-{satellite}\\batch-1"
first = CloudCatcher(target_dir_name, satellite)
first.start(datetime(2022, 1, 31, 14), 3, 1)