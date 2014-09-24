from util import *
import random
import math


angles = LinearSegmentedColormap.from_list('angles', ('r', 'g', 'b', 'y', 'r'))

#sm = ScalarMappable(cmap=angles)
#sm.set_clim(-np.pi, np.pi)




def gen_data ():
  data = np.zeros((50,50), complex)
  for y in range(-25,25):
    for x in range(-25,25):
      data[y+25, x+25] = cmath.rect(random.triangular(), math.atan2(y,x))

  return data

data = gen_data()

im = plt.imshow(complex_color(data), interpolation='none') #, cmap=angles)

def updatefig (j):
  data = gen_data()
  im.set_data(complex_color(data))

  #return (im,)

# kick off the animation
frames = 32
loop_time = 1
ani = animation.FuncAnimation(plt.gcf(), updatefig, frames=frames,
                              interval=loop_time/frames*1000, blit=False)
style_and_show()
