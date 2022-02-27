import os
from goes2go.data import goes_nearesttime
import matplotlib.pyplot as plt
from cloud_catcher.lib import ensure_dir
from goes2go.rgb import load_RGB_channels
import gc
from datetime import datetime
import numpy


class CloudCatcher:
    def __init__(self, dir, data_save_dir, satellite, dpi, band):
        self.dir = dir
        self.data_save_dir = data_save_dir
        self.satellite = satellite
        self.dpi = dpi
        self.band = band
        ensure_dir(dir)

    def __save_image(self,  target_path, photo):
        print('SAVING TO: ', target_path)
        imshow_args = {
            'interpolation': 'none',
            'cmap': 'Greys'
        }
        band_str = 'CMI_C' + '%02d' % self.band

        plt.style.use('dark_background')
        plt.gcf().set_facecolor("black")

        ax = plt.axes(projection=photo.rgb.crs)
        ax.imshow(photo[band_str], **imshow_args)
        ax.coastlines(linewidth=10)

        plt.savefig(target_path, dpi=self.dpi, bbox_inches='tight',
                    facecolor='black', edgecolor='none')
        # this is garbage
        del photo
        plt.close('all')
        gc.collect()

    def __get_photo_from(self, date):
        try:
            photo = goes_nearesttime(date,
                                     satellite=self.satellite,
                                     product='ABI',
                                     overwrite=False,
                                     domain='F',
                                     save_dir=self.data_save_dir,
                                     return_as='xarray')
        except Exception:
            photo = False
        return photo

    def start(self, date):
        photo = self.__get_photo_from(date)
        photo_time = numpy.array2string(
            photo['time_coverage_end']).replace('\'', '')
        photo_name = datetime.strptime(
            photo_time,
            '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%Y%m%dT%H%M%S")
        target_path = os.path.join(
            self.dir, f"{photo_name}.png").replace("\\", "/")
        if os.path.exists(target_path):
            return ('photo exists', photo_name)
        print('Saving', target_path)
        if photo:
            self.__save_image(target_path, photo)
            return (True, photo_name)
        return (False, photo_name)
