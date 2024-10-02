from sklearn.decomposition import FastICA, NMF
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread
from scipy.stats import pearsonr

# Define the input TIFF file path
tiff_file = '/Users/karlfrontzek/Library/Mobile Documents/com~apple~CloudDocs/Documents/UCL/project/pdMicroglia/image analysis pipeline/241001_spectralunmixing/P85-19_16_CD74.small.tif'

# Load the TIFF file (assuming multiple channels)
image = imread(tiff_file)
image_c2 = image[:, :, 1]  # Channel 2
image_c3 = image[:, :, 2]  # Channel 3
image_c4 = image[:, :, 3]  # Channel 4

# Reshape images into pixel spectra (each pixel is a spectrum across channels)
pixels = image_c2.size
observed_spectrum = np.stack([image_c2.flatten(), image_c3.flatten(), image_c4.flatten()], axis=-1)

# Perform Independent Component Analysis (ICA) on channel 2
ica = FastICA(n_components=3,random_state=20,max_iter=1000) # >>> RANDOM STATE 20!!!!!
ica_W = ica.fit_transform(observed_spectrum)  # Abundances
ica_unmixed_image_c2 = ica_W[:, 0].reshape(image_c2.shape)

# Perform Non-negative Matrix Factorization (NMF) on channel 3
nmf = NMF(n_components=3, init='random', random_state=0, max_iter=1000)
nmf_W = nmf.fit_transform(observed_spectrum)  # Abundances
nmf_unmixed_image_c3 = nmf_W[:, 1].reshape(image_c3.shape)

# Save the unmixed images
plt.imsave('ica_unmixed_c2.png', ica_unmixed_image_c2, cmap='gray')
plt.imsave('nmf_unmixed_c3.png', nmf_unmixed_image_c3, cmap='gray')

print("ICA and NMF processing completed and images saved.")


# Assuming the images are in numpy arrays: nmf_unmixed_image_c3 and ica_unmixed_image_c2
# 1. Invert the ica_unmixed_image_c2
ica_inverted_image_c2 = np.max(ica_unmixed_image_c2) - ica_unmixed_image_c2

# 2. Define the rolling ball background subtraction using white_tophat
# You can adjust the size of the structuring element (ball radius)
ball_radius = 50  # Adjust this value according to your needs

# Apply background subtraction using 'footprint' instead of 'selem'
ica_subtracted_image_c2 = white_tophat(ica_inverted_image_c2, footprint=disk(ball_radius))
nmf_subtracted_image_c3 = white_tophat(nmf_unmixed_image_c3, footprint=disk(ball_radius))

# 3. Plot the results
plt.figure(figsize=(10, 10))

# First row - original images
plt.subplot(2, 2, 1)  # 2 rows, 2 columns, 1st subplot
plt.imshow(nmf_unmixed_image_c3, cmap='gray')
plt.title('Original NMF Unmixed Image C3')
plt.axis('off')

plt.subplot(2, 2, 2)  # 2 rows, 2 columns, 2nd subplot
plt.imshow(ica_unmixed_image_c2, cmap='gray')
plt.title('Original ICA Unmixed Image C2')
plt.axis('off')

# Second row - processed images
plt.subplot(2, 2, 3)  # 2 rows, 2 columns, 3rd subplot
plt.imshow(nmf_subtracted_image_c3, cmap='gray')
plt.title('Background Subtracted NMF Image C3')
plt.axis('off')

plt.subplot(2, 2, 4)  # 2 rows, 2 columns, 4th subplot
plt.imshow(ica_subtracted_image_c2, cmap='gray')
plt.title('Inverted + Background Subtracted ICA Image C2')
plt.axis('off')

plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()

# 4. Colocalization calculations

# Ensure the images are flattened for colocalization calculations
ica_flat = ica_subtracted_image_c2.flatten()
nmf_flat = nmf_subtracted_image_c3.flatten()

#  Pearson's Correlation Coefficient
pearson_corr, _ = pearsonr(nmf_flat, ica_flat)
print(f"Pearson's Correlation Coefficient: {pearson_corr}")
