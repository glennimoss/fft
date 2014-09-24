from collections import Counter
from PIL import Image
import cmath
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, rgb_to_hsv, hsv_to_rgb
from matplotlib import animation

angles = LinearSegmentedColormap.from_list('angles', ('r', 'g', 'b', 'y', 'r'))

def complex_color (data, vmin=0, vmax=1, normalize=False, scale_value=True):
  colorized = angles(np.angle(data)/(2*np.pi) + 0.5)

  if not scale_value:
    return colorized

  hsv = rgb_to_hsv(colorized[:,:,:3])

  data = np.abs(data)
  if normalize:
    vmin = data.min()
    vmax = data.max()

  hsv[...,2].flat = (data.clip(vmin,vmax) + vmin)/(vmax - vmin)

  return hsv_to_rgb(hsv)

def imshow (data, **kwargs):
  return plt.imshow(data, interpolation="none", cmap="gray", **kwargs)

def show_fft_mag (data, shift=True, log=False, vmin=0, vmax=1):
  #plt.imshow(np.log(np.abs(np.fft.fftshift(data))), interpolation="none", cmap='gray')
  if shift:
    data = np.fft.fftshift(data)
  data = np.abs(data)
  if log:
    data = np.log(data)
  return plt.imshow(data, interpolation="none", cmap='gray', vmin=vmin, vmax=vmax)

def update_fft_mag (im, data, normalize=False):
  data = np.abs(data)
  data = np.fft.fftshift(data)
  if normalize:
    im.set_clim(data.min(), data.max())

  im.set_data(data)

def show_fft_phase (data, shift=True, **kwargs):
  if shift:
    data = np.fft.fftshift(data)
  return plt.imshow(complex_color(data, **kwargs), interpolation='none')

def update_fft_phase (im, data, shift=True, **kwargs):
  if shift:
    data = np.fft.fftshift(data)
  im.set_data(complex_color(data, *im.get_clim(), **kwargs))


def circle (x0, y0, r):
  x = r
  y = 0
  rerr = 1 - x

  while x >= y:
    yield x + x0, y + y0
    yield (y + x0, x + y0)
    yield (-x + x0, y + y0)
    yield (-y + x0, x + y0)
    yield (-x + x0, -y + y0)
    yield (-y + x0, -x + y0)
    yield (x + x0, -y + y0)
    yield (y + x0, -x + y0)
    y += 1
    if rerr < 0:
      rerr += 2*y + 1
    else:
      x -= 1
      rerr += 2*(y - x + 1)


def plots (rows, columns, col_labels=None, row_labels=None):
  #fig, axes = plt.subplots(rows, columns, sharex=True, sharey=True)

  #return fig, (a for row in axes for a in row)
  for p in range(rows*columns):
    sp = plt.subplot(rows, columns, p+1)

    if col_labels and p < columns:
      plt.xlabel(col_labels[p])
      plt.gca().xaxis.set_label_position('top')

    if row_labels and p % columns == 0:
      plt.ylabel(row_labels[p//columns])

    yield sp

def style_and_show (grid=False):
  for a in plt.gcf().axes:
    if grid:
      height, width = a.get_images()[0].get_size()
      a.set_xticks([t-0.5 for t in range(width)])
      a.set_yticks([t-0.5 for t in range(height)])
      a.grid(color='green', linestyle='-', alpha=0.5)
    else:
      a.set_xticks([])
      a.set_yticks([])
      for sp in a.spines.values():
        sp.set_visible(False)
    a.set_xticklabels([])
    a.set_yticklabels([])
    a.tick_params('both', direction='out')

  plt.subplots_adjust(left=0, bottom=0.02, right=1, top=0.95, wspace=0.1, hspace=0.1)

  plt.show()
