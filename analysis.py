from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# Import entries, should be a list of tuples in the format (file name, rotation, error in rotation).
from settings import entries

data = np.array(entries)

# Create necessary Matplotlib objects
figure, axis = plt.subplots(len(entries), 2, tight_layout=True)

# Load data
rotations = data[:, 1].astype(np.float)
rotations_err = data[:, 2].astype(np.float)

# Prepare Numpy arrays we'll use later
intensities = np.empty((len(entries), 1))
intensities_err = np.empty((len(entries), 1))

# Timestamp for files
timestamp = datetime.now().strftime('%d-%m@%H-%M-%S')

# Loop over the various entries
for i in range(len(entries)):
    # Get the image file name
    file_name = entries[i][0]
    # Load the image
    image = Image.open(file_name)

    # Tell the user which file we are processing
    print(f'Processing image: {file_name}, has dimensions: {image.size}')

    # Determine the intensity of each pixel
    intensity = np.max(np.asarray(image), 2)

    # Plot the raw image
    axis[i, 0].imshow(image)
    axis[i, 0].set_title(file_name)

    # Plot the intensity
    axis[i, 1].imshow(intensity, cmap='gray')
    axis[i, 1].set_title(f'{file_name} intensity')

    # Save the intensities to their array
    mean_intensity = np.mean(intensity)
    intensities[i] = mean_intensity
    mean_intensity_err = np.std(intensity)
    intensities_err[i] = mean_intensity_err

    # Print additional information for the user
    print(
        f'Average intensity: {mean_intensity:.1e}±{mean_intensity_err:.0e} for rotation: {rotations[i]:.1e}±{rotations_err[i]:.0e}°')
    print(
        f'TeX friendly: {rotations[i]:.1e}±{rotations_err[i]:.0e}° & {mean_intensity:.1e}±{mean_intensity_err:.0e} \\\\')

# Save the figure maps
plt.savefig(f'figures/maps-{timestamp}.svg')
plt.show()

# Determine the maximum intensity
I0 = np.max(intensities)
# Calculate the relative intensities
relative_intensities = intensities / I0
# Determine the error in the relative intensities
relative_intensities_err = (1 / I0) * np.sqrt(
    np.square(intensities_err) + np.square(intensities_err[np.argmax(intensities)]) / np.square(I0))

# Plot the intensity of rotation
plt.title('Intensity vs. rotation')
plt.grid()
plt.errorbar(rotations, relative_intensities, relative_intensities_err, rotations_err)
plt.xlabel('Rotation [°]')
plt.ylabel(r'Intensity ($I/I_0$) [unit less]')

# Save the plot
plt.savefig(f'figures/plot-{timestamp}.svg')
plt.show()
