def ensure_dir(dir):
    import os
    if not os.path.exists(dir):
        os.makedirs(dir)


def create_grid(x, y, steps, data=False, u=False, v=False, ):
    from scipy import interpolate
    import numpy

    xi = numpy.linspace(x.min().item(),
                        x.max().item(), steps)
    yi = numpy.linspace(y.min().item(),
                        y.max().item(), steps)
    X, Y = numpy.meshgrid(xi, yi)
    if u:
        u = interpolate.griddata((x, y), u, (X, Y), method='cubic')
        u = numpy.nan_to_num(u)
    if v:
        v = interpolate.griddata((x, y), v, (X, Y), method='cubic')
        v = numpy.nan_to_num(v)

    if data:
        data = interpolate.griddata(
            (x, y), data, (X, Y), method='cubic')
        data = numpy.nan_to_num(data)
    return (X, Y, steps, data, u, v)


def mask_data(x, y, ws, wd, max_coords):
    # -- transform function and graph functions
    mask = (x > max_coords['south']) & (x < max_coords['north']) & (
        y > max_coords['west']) & (y < max_coords['east'])
    ws = ws.where(mask, drop=True)
    wd = wd.where(mask, drop=True)
    x = x.where(mask, drop=True)
    y = y.where(mask, drop=True)
    return x, y, ws, wd


def setup_graph(projection, extent):
    import matplotlib.pyplot as plt
    # -- set up graph
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(10, 10), edgecolor='black')
    print('seting up', projection)
    ax = fig.add_subplot(projection=projection, extent=extent,
                         snap=True, frame_on=False)
    return ax


def get_uv(wind_speed, wind_direction):
    import numpy
    # - Wind-UV Components - http://colaweb.gmu.edu/dev/clim301/lectures/wind/wind-uv
    u = -wind_speed * \
        numpy.sin(numpy.radians(wind_direction))
    v = -wind_speed * \
        numpy.cos(numpy.radians(wind_direction))
    return u, v


def debug(attrs):
    print('DEBUG')
    print('\n \033[92m--------------\033[0m \n'.join("%s: %s" %
          item for item in attrs.items()))
