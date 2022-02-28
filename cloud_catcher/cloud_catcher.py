# ------------ STEP 2: start downloading! skip to catch function
import os
from goes2go.data import goes_nearesttime
import matplotlib.pyplot as plt
from cloud_catcher.lib import ensure_dir
from goes2go.rgb import load_RGB_channels
import gc
from datetime import datetime
import numpy
import cartopy.crs as ccrs


class CloudCatcher:
    def __init__(self, dir, data_save_dir, satellite, dpi, band, cmap):
        self.dir = dir
        self.data_save_dir = data_save_dir
        self.satellite = satellite
        self.dpi = dpi
        self.band = band
        self.cmap = cmap
        ensure_dir(dir)

    def __save_image(self,  target_path, photo):
        print('SAVING TO: ', target_path)
        # https: // scitools.org.uk/cartopy/docs/latest/reference/projections.html
        target_projection = ccrs.EquidistantConic(
            central_longitude=-32.46, central_latitude=37.54)
        imshow_args = {
            **photo.rgb.imshow_kwargs,
            'cmap': self.cmap,
            'transform': photo.rgb.crs,
            'interpolation': 'kaiser'
            # https://matplotlib.org/stable/gallery/images_contours_and_fields/interpolation_methods.html
        }
        fig = plt.figure(figsize=(10, 10), edgecolor='black')
        plt.style.use('dark_background')
        band_str = 'CMI_C' + '%02d' % self.band
        ax = fig.add_subplot(projection=target_projection)
        ax.set_extent([-120, 0, 0, 80])

        ax.imshow(photo[band_str], **imshow_args)
        ax.coastlines(linewidth=0.3, color="#00FF66", alpha=1)
        fig.subplots_adjust(wspace=0.01)
        plt.savefig(target_path, dpi=self.dpi, bbox_inches='tight',
                    facecolor='black', edgecolor='black')
        # this is garbage
        plt.close('all')
        gc.collect()
        del photo

    def __get_photo_from_date(self, date):
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

    def catch(self, date):
        # download .n and get the xarray data file
        photo = self.__get_photo_from_date(date)
        if not photo:
            return (False, date)
        photo_time = numpy.array2string(
            photo['time_coverage_end']).replace('\'', '')
        photo_name = datetime.strptime(
            photo_time,
            '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%Y%m%dT%H%M%S")
        target_path = os.path.join(
            self.dir, f"{photo_name}.png").replace("\\", "/")
        if os.path.exists(target_path):
            return ('photo exists', photo_name)
        if photo:
            # ------------  STEP 3: save the image! line 22
            self.__save_image(target_path, photo)
            return (True, photo_name)
        return (False, photo_name)
