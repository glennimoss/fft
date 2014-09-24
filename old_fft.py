from util import *
import sys

filename = 'icon-data-analytics.png'
if len(sys.argv) > 1:
  filename = sys.argv[1]

im = Image.open(filename)
shape = (im.size[1], im.size[0])
red_data = np.asarray(im.getdata().getband(0)).reshape(shape)
green_data = np.asarray(im.getdata().getband(1)).reshape(shape)
blue_data = np.asarray(im.getdata().getband(2)).reshape(shape)
alpha_data = np.asarray(im.getdata().getband(3)).reshape(shape)

plot = plots(5, 4,
    row_labels=('Image', 'FFT Magnitude', 'FFT Phase', 'IFFT Image', 'Orig/Inv Diff'),
    col_labels=('Red', 'Green', 'Blue', 'Alpha'))


next(plot)
imshow(red_data)

#plt.ylabel('Image')
#plt.xlabel('Red')
#plt.gca().xaxis.set_label_position('top')

next(plot)
imshow(green_data)

#plt.xlabel('Green')
#plt.gca().xaxis.set_label_position('top')

next(plot)
imshow(blue_data)

#plt.xlabel('Blue')
#plt.gca().xaxis.set_label_position('top')

next(plot)
imshow(alpha_data)

#plt.xlabel('Alpha')
#plt.gca().xaxis.set_label_position('top')

print("fft red channel...")
fft_rdata = np.fft.fft2(red_data)
print("fft green channel...")
fft_gdata = np.fft.fft2(green_data)
print("fft blue channel...")
fft_bdata = np.fft.fft2(blue_data)
print("fft alpha channel...")
fft_adata = np.fft.fft2(alpha_data)

# fft magnitude
next(plot)
show_fft_mag(fft_rdata, log=True, vmin=None, vmax=None)

#plt.ylabel('FFT Magnitude')

next(plot)
show_fft_mag(fft_gdata, log=True, vmin=None, vmax=None)

next(plot)
show_fft_mag(fft_bdata, log=True, vmin=None, vmax=None)

next(plot)
show_fft_mag(fft_adata, log=True, vmin=None, vmax=None)


# fft phase
next(plot)
show_fft_phase(fft_rdata)

#plt.ylabel("FFT Phase")

next(plot)
show_fft_phase(fft_gdata)

next(plot)
show_fft_phase(fft_bdata)

next(plot)
show_fft_phase(fft_adata)


# Back to orig:

print("ifft red channel...")
new_red = np.abs(np.fft.ifft2(fft_rdata))
print("ifft green channel...")
new_green = np.abs(np.fft.ifft2(fft_gdata))
print("ifft blue channel...")
new_blue = np.abs(np.fft.ifft2(fft_bdata))
print("ifft alpha channel...")
new_alpha = np.abs(np.fft.ifft2(fft_adata))

red_diff = np.abs(new_red - red_data)
green_diff = np.abs(new_green - green_data)
blue_diff = np.abs(new_blue - blue_data)
alpha_diff = np.abs(new_alpha - alpha_data)

print("max red diff:", red_diff.max())
print("max green diff:", green_diff.max())
print("max blue diff:", blue_diff.max())
print("max alpha diff:", alpha_diff.max())

next(plot)
imshow(new_red)

#plt.ylabel("IFFT Image")

next(plot)
imshow(new_green)

next(plot)
imshow(new_blue)

next(plot)
imshow(new_alpha)


next(plot)
imshow(red_diff, vmin=0, vmax=255)

#plt.ylabel('Original/Inverse Diff')

next(plot)
imshow(green_diff, vmin=0, vmax=255)

next(plot)
imshow(blue_diff, vmin=0, vmax=255)

next(plot)
imshow(alpha_diff, vmin=0, vmax=255)

style_and_show()

