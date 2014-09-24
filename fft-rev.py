from util import *
import math
from scipy.misc import imresize, imrotate

size = 100
frames = 100
loop_time = 5

#freq_mag = 1
freq_mag = 5025.380963681708



def fiter (f):
  return range(int(math.floor(f)), int(math.ceil(f))+1)


def cycle_phase (frame):
  step = frame/frames
  fft = np.zeros((size, size), np.complex)
  fft[0][0] = freq_mag
  #fft[0][5] = freq_mag
  #ifft = np.fft.ifft2(fft)
  ifft = np.array(fft)
  ifft[:] = [math.sin(2*math.pi*(x + frame)/size)/2+0.5 for x in range(size)]



  refft = np.fft.fft2(np.abs(ifft))
  small_img = np.abs(np.fft.ifft2(refft))
  small_refft = np.fft.fft2(small_img)

  return fft, ifft, refft, small_img, small_refft

def cycle_freq (frame):
  step = frame/frames
  fft = np.zeros((size, size), np.complex)
  fft[0][0] = freq_mag
  #fft[0][5] = freq_mag
  #ifft = np.fft.ifft2(fft)
  ifft = np.array(fft)
  ifft[:] = [math.sin(2*math.pi*x/size*(frame+1))/2+0.5 for x in range(size)]



  refft = np.fft.fft2(np.abs(ifft))
  #print(refft[0]*(1-np.isclose(refft[0], 0)))
  small_img = np.fft.ifft2(refft)
  small_refft = np.fft.fft2(small_img)

  return fft, ifft, refft, small_img, small_refft

def cycle_skew (frame):
  step = frame/frames
  fft = np.zeros((size, size), np.complex)
  fft[0][0] = freq_mag
  #fft[0][5] = freq_mag
  #ifft = np.fft.ifft2(fft)
  ifft = np.array(fft)
  f = 5
  for y in range(size):
    ystep = y/size
    ifft[y] = [math.sin(f * 2*math.pi*(x + frame*ystep)/size)/2+0.5 for x in range(size)]



  refft = np.fft.fft2(np.abs(ifft))
  #print(refft[0]*(1-np.isclose(refft[0], 0)))
  small_img = np.fft.ifft2(refft)
  small_refft = np.fft.fft2(small_img)

  return fft, ifft, refft, small_img, small_refft



gen_data = cycle_skew

#imgmax = np.max(np.abs(gen_data(frames-1)[1]))
#imgmax = 0.000434027777778
imgmax = 1

plot = plots(2,5, col_labels=('FFT', 'Image', 'Re-FFT', 'Small', 'Small FFT'),
    row_labels=('Magnitude', 'Phase'))

#fft, img = gen_data(0)
fft, ifft, refft, small_img, small_refft = gen_data(0)

next(plot)
im_mag = show_fft_mag(fft, vmax=freq_mag)

next(plot)
#im_img = imshow(img, vmin=0, vmax=imgmax)
im_img = imshow(np.abs(ifft), vmin=0, vmax=imgmax)
#im_img = show_fft_mag(ifft, False)

next(plot)
im_refft = show_fft_mag(refft, vmax=freq_mag)

next(plot)
im_small_img = imshow(np.abs(small_img), vmin=0, vmax=imgmax)

next(plot)
im_small_refft = show_fft_mag(small_refft) #, vmax=freq_mag)

next(plot)
im_phase = show_fft_phase(fft, normalize=True)

next(plot)
im_img_phase = show_fft_phase(ifft, False, normalize=False)

next(plot)
im_refft_phase = show_fft_phase(refft, normalize=True)

next(plot)
im_small_img_phase = show_fft_phase(small_img, False, normalize=False)

next(plot)
im_small_refft_phase = show_fft_phase(small_refft, normalize=True)


def updatefig (j):
  fft, ifft, refft, small_img, small_refft = gen_data(j)

  update_fft_mag(im_mag, fft)
  update_fft_phase(im_phase, fft, normalize=True)

  im_img.set_data(np.abs(ifft))
  update_fft_phase(im_img_phase, ifft, False, normalize=False)

  update_fft_mag(im_refft, refft)
  update_fft_phase(im_refft_phase, refft, normalize=True)

  im_small_img.set_data(np.abs(small_img))
  update_fft_phase(im_small_img_phase, small_img, False, normalize=False)

  update_fft_mag(im_small_refft, small_refft, normalize=True)
  update_fft_phase(im_small_refft_phase, small_refft, normalize=True)

  # blit=False don't need to return
  #return im_mag, im_phase, im_img, im_img_phase, im_refft, im_refft_phase

# kick off the animation
ani = animation.FuncAnimation(plt.gcf(), updatefig, frames=frames,
                              interval=loop_time/frames*1000, blit=False)


style_and_show()
