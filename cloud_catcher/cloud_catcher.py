# ------------ STEP 2: start downloading! skip to catch function
import os
import re
from goes2go.data import goes_nearesttime
import matplotlib.pyplot as plt
from cloud_catcher.lib import ensure_dir, debug, mask_data, get_uv, setup_graph
import gc
from datetime import datetime
import numpy
import cartopy.crs as ccrs
from toolbox.cartopy_tools import pc

profiling = True


class CloudCatcher:
    def __init__(self, dir, data_save_dir, satellite, dpi, band, cmap):
        self.dir = dir
        self.data_save_dir = data_save_dir
        self.satellite = satellite
        self.dpi = dpi
        self.band = band
        self.cmap = cmap
        ensure_dir(dir)

    def catch(self, date):
        # download .n and get the xarray data file

        photo = self.__get_photo_from_date(date)
        wind = self.__get_wind_data_from_date(date)

        # - something went wrong downloading the data
        if not photo or not wind:
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
            self.__save_image(target_path, photo, wind)
            return (True, photo_name)
        return (False, photo_name)

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

    def __get_wind_data_from_date(self, date):
        try:
            data = goes_nearesttime(date,
                                    satellite=self.satellite,
                                    product='ABI-L2-DMWVF',
                                    overwrite=False,
                                    save_dir=self.data_save_dir,
                                    return_as='xarray')
        except Exception:
            data = False
        return data

    def __save_image(self,  target_path, photo, wind):
        print('Processing ', target_path)
        # - Projections - https: // scitools.org.uk/cartopy/docs/latest/reference/projections.html
        target_projection = ccrs.EquidistantConic(
            central_longitude=-32.46, central_latitude=46.54)
        imshow_args = {
            **photo.rgb.imshow_kwargs,
            'cmap': self.cmap,
            'transform': photo.rgb.crs,
            'interpolation': 'kaiser',
            # - Interpolation methods - https://matplotlib.org/stable/gallery/images_contours_and_fields/interpolation_methods.html
        }
        max_coords = {
            'north': 61,
            'south': 4,
            'west': -102,
            'east': 0
        }
        band_str = 'CMI_C%02d' % self.band
        photo_crop_bounds = [-120, 0, 0, 80]  # lon E, lon W, lat S,lat N

        # for possibly future use
        # linspace_steps = 10
        # from cloud_catcher/lib import create_grid
        # create_grid()

        def get_time():
            return datetime.now().strftime("%H:%M:%S")

        ax = setup_graph(target_projection, photo_crop_bounds)

        x, y, wind_speed, wind_direction = mask_data(
            wind.wind_speed.lat, wind.wind_speed.lon, wind.wind_speed, wind.wind_direction, max_coords)
        u, v = get_uv(wind_speed, wind_direction)

        wind_speed_data = numpy.sqrt(u**2+v**2)
        wind_speed_data = numpy.nan_to_num(wind_speed_data)

        # -- draw wind
        # stream_lw = 2*SPD / SPD.max()
        # linewidth = stream_lw m
        if profiling:
            print('Plotting...', get_time())
        plt.quiver(x, y,
                   u, v, wind_speed_data, pivot='mid', transform=pc, cmap='jet')

        # -- draw photo
        if profiling:
            print('drawing photo', get_time())
        ax.imshow(photo[band_str], **imshow_args)
        ax.coastlines(linewidth=0.3, color="#00FF66", alpha=1)

        # ---
        print('Saving image: ', target_path)
        # plt.show()
        plt.savefig(target_path, dpi=self.dpi, bbox_inches='tight',
                    facecolor='black', edgecolor='black')
        # -- this is garbage
        plt.close('all')
        gc.collect()
        del photo
