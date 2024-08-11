from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Load an image
image_path = '3\\task1\hello.jpg'
image = Image.open(image_path)

# Convert the image to a NumPy array
image_np = np.array(image)

# Separate the color channels
r_channel = image_np[:, :, 0]
g_channel = image_np[:, :, 1]
b_channel = image_np[:, :, 2]

# Calculate histograms for each channel
r_hist, r_bins = np.histogram(r_channel.flatten(), bins=256, range=[0, 256])
g_hist, g_bins = np.histogram(g_channel.flatten(), bins=256, range=[0, 256])
b_hist, b_bins = np.histogram(b_channel.flatten(), bins=256, range=[0, 256])

# Plot histograms
plt.figure(figsize=(10, 4))

# Red channel histogram
plt.subplot(131)
plt.plot(r_bins[:-1], r_hist, color='red')
plt.title('Red Channel')
plt.xlim([0, 256])

# Green channel histogram
plt.subplot(132)
plt.plot(g_bins[:-1], g_hist, color='green')
plt.title('Green Channel')
plt.xlim([0, 256])

# Blue channel histogram
plt.subplot(133)
plt.plot(b_bins[:-1], b_hist, color='blue')
plt.title('Blue Channel')
plt.xlim([0, 256])

plt.tight_layout()
plt.show()
