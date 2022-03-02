# ------------ STEP 2: start downloading! skip to catch function on the bottom
import os
from goes2go.data import goes_nearesttime
import matplotlib.pyplot as plt
from cloud_catcher.lib import ensure_dir
import gc
from datetime import datetime
import numpy
import cartopy.crs as ccrs
from toolbox.cartopy_tools import pc
from scipy import interpolate


class CloudCatcher:
    def __init__(self, dir, data_save_dir, satellite, dpi, band, cmap):
        self.dir = dir
        self.data_save_dir = data_save_dir
        self.satellite = satellite
        self.dpi = dpi
        self.band = band
        self.cmap = cmap
        ensure_dir(dir)

    def __save_image(self,  target_path, photo, wind):
        print('Processing ', target_path)
        print(*wind)
        print(wind.wind_vectors_in_atmospheric_layer[0:2000:100])
        print(wind.mean_cloud_top_pressure_in_atmospheric_layer)
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

        def get_time():
            return datetime.now().strftime("%H:%M:%S")

        # -- vars and transforms
        linspace_steps = 10
        print('masking', get_time())
        mask = (wind.wind_speed.lat > max_coords['south']) & (wind.wind_speed.lat < max_coords['north']) & (
            wind.wind_speed.lon > max_coords['west']) & (wind.wind_speed.lon < max_coords['east'])
        wind_speed = wind.maximum_wind_speed.where(mask, drop=True)
        # wind_speed = wind.wind_speed.where(
        #     ~numpy.isnan(wind.wind_speed), drop=True)
        wind_direction = wind.wind_direction.where(mask, drop=True)
        # wind_direction = wind.wind_speed.where(
        #     ~numpy.isnan(wind.wind_speed), drop=True)
        x = wind.lon.where(mask, drop=True)
        # x = wind.wind_speed.where(~numpy.isnan(wind.wind_speed), drop=True)
        y = wind.lat.where(mask, drop=True)
        # y = wind.wind_speed.where(~numpy.isnan(wind.wind_speed), drop=True)
        # -- set up graph
        plt.style.use('dark_background')
        fig = plt.figure(figsize=(10, 10), edgecolor='black')
        ax = fig.add_subplot(projection=target_projection,
                             snap=True, frame_on=False)
        ax.set_extent(photo_crop_bounds)

        print('making grid...', get_time())
        # - Wind-UV Components - http://colaweb.gmu.edu/dev/clim301/lectures/wind/wind-uv
        u = -wind_speed * \
            numpy.sin(numpy.radians(wind_direction))
        v = -wind_speed * \
            numpy.cos(numpy.radians(wind_direction))
        SPD = numpy.sqrt(u**2+v**2)
        SPD = numpy.nan_to_num(SPD)

        # levels = MaxNLocator(nbins=15).tick_values(
        #     wind.wind_speed.min(), wind.wind_speed.max())
        # -- draw wind
        # speed_norm = plt.Normalize(0.0, SPD.max())

        print('u')
        # norm=speed_norm
        # stream_lw = 2*SPD / SPD.max()
        # linewidth = stream_lw m
        print('Plotting...', get_time())
        plt.quiver(wind_speed.lon, wind_speed.lat,
                   u, v, SPD, pivot='mid', transform=pc, cmap='jet')
        # **cm_wind().cmap_kwargs,

        # -- draw photo
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

    def catch(self, date):
        # download .n and get the xarray data file
        photo = self.__get_photo_from_date(date)
        wind = self.__get_wind_data_from_date(date)
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
