import os
from goes2go.data import goes_nearesttime
import matplotlib.pyplot as plt
from lib import ensure_dir


class CloudCatcher:
    def __init__(self, dir, data_save_dir, satellite, dpi):
        print('--- INIT CLOUDCATCHER ---')
        self.dir = dir
        self.data_save_dir = data_save_dir
        self.satellite = satellite
        self.dpi = dpi
        ensure_dir(dir)

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
        plt.savefig(target_path, dpi=self.dpi, bbox_inches='tight',
                    facecolor='black', edgecolor='none')
        plt.close('all')

    def __get_photo_from(self, date):
        return goes_nearesttime(date,
                                satellite=self.satellite,
                                product='ABI',
                                overwrite=False,
                                domain='F',
                                save_dir=self.data_save_dir,
                                return_as='xarray')

    def start(self, date):
        photo_name = date.strftime("%Y%m%dT%H%M")
        photo = self.__get_photo_from(date)
        self.__save_image(photo_name, photo)
        return photo_name
