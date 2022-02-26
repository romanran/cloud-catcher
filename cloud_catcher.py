import os
from goes2go.data import goes_nearesttime
import matplotlib.pyplot as plt
from datetime import timedelta
from lib import ensure_dir

class CloudCatcher:
    def __init__(self, dir, satellite):
        self.dir = dir
        self.satellite = satellite
        ensure_dir(dir)

    def __get_photo_from(self, shot_date):
        return goes_nearesttime(shot_date,
                                satellite=self.satellite,
                                product='ABI',
                                overwrite=False,
                                domain='F',
                                return_as='xarray')
    def __save_image(self,  photo_name, photo):
        target_path = os.path.join(
            self.dir, f"{photo_name}.png").replace("\\", "/")
        print('SAVING TO: ', target_path)

        imshow_args = {'extent': [-5433893.0, 5433893.0, -5433893.0,
                                  5433893.0], 'origin': 'upper', 'interpolation': 'antialiased'}
        ax = plt.axes(projection=photo.rgb.crs)
        source = photo.rgb.NaturalColor(
            gamma=1, pseudoGreen=True, night_IR=True)
        ax.imshow(source, **imshow_args)

        ax.coastlines(linewidth=0.1)
        plt.savefig(target_path, dpi=1600, bbox_inches='tight',
                    facecolor='black', edgecolor='none')


    def start(self, start_date, step_hours, no_of_photos):
        for x in range(no_of_photos):
            shot_date = start_date + timedelta(hours=step_hours * x)
            photo_name = shot_date.strftime("%Y_%m_%d-%H")
            photo = self.__get_photo_from(shot_date)
            self.__save_image(photo_name, photo)
