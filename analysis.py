from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from sklearn.metrics import mean_squared_error

# Import entries, should be a list of tuples in the format (file name, rotation, error in rotation)
# and various configurations.
from settings import compare, create_map, entries, map_values


def remap(values: np.ndarray, minimum: float, maximum: float) -> np.ndarray:
    return (values - minimum) / (maximum - minimum)


data = np.array(entries)

if create_map:
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
    image = np.array(Image.open(file_name))

    # Tell the user which file we are processing
    print(f'Processing image: {file_name}, has dimensions: {image.size}')

    # Determine the intensity of each pixel (this excludes alpha values.
    intensity = np.max(np.array(image)[:, :, :3], 2)

    if create_map:
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
        f'TeX friendly: ${rotations[i]:.1e}\pm{rotations_err[i]:.0e}\degrees$ & ${mean_intensity:.1e}\pm{mean_intensity_err:.0e}$ \\\\')

if create_map:
    # Save the figure maps
    plt.savefig(f'figures/maps-{timestamp}.jpg')
    plt.show()

# Determine the maximum intensity
I_max = np.max(intensities)
I_max_err = intensities_err[np.argmax(intensities)]
if map_values:
    # Determine the minimum intensity
    I_min = np.min(intensities)
    I_min_err = intensities_err[np.argmin(intensities)]
    # Calculate the relative intensities
    relative_intensities = remap(intensities, I_min, I_max)[:, 0]
    # Determine the error in the relative intensities
    relative_intensities_err = (np.sqrt((1 / (I_max - I_min) * intensities_err) ** 2 + (
            (intensities - I_max) / (I_max - I_min) ** 2 * I_min_err) ** 2 + (
                                                (I_min - intensities) / (I_max - I_min) ** 2 * I_max_err) ** 2))[:, 0]
else:
    # Calculate the relative intensities
    relative_intensities = (intensities / I_max)[:, 0]
    # Determine the error in the relative intensities
    relative_intensities_err = ((1 / I_max) * np.sqrt(
        np.square(intensities_err) + np.square(I_max_err) / np.square(I_max)))[:, 0]

# Plot the intensity of rotation
plt.title('Intensity vs. rotation')
plt.grid()
plt.errorbar(rotations, relative_intensities, relative_intensities_err, rotations_err, label='Measurement')
plt.xlabel('Rotation [°]')
if map_values:
    plt.ylabel(r'Relative intensity ($I$ mapped between $I_{max}$ and $I_{min}$) [unit less]')
else:
    plt.ylabel(r'Intensity ($I/I_0$) [unit less]')

if compare:
    samples = np.linspace(np.min(rotations), np.max(rotations), 500)
    plt.plot(samples, np.cos(np.deg2rad(samples)) ** 2, label='Prediction')
    plt.legend()

    MSE = mean_squared_error(relative_intensities - np.cos(np.deg2rad(rotations)) ** 2, np.zeros(np.shape(rotations)))
    print(f'MSE between measurement and prediction: {MSE:.1e}')

# Save the plot
plt.savefig(f'figures/plot-{timestamp}.svg')
plt.show()

if compare:
    plt.title('Deviation from expected result')
    plt.errorbar(rotations, relative_intensities - np.cos(np.deg2rad(rotations)) ** 2, relative_intensities_err)
    plt.xlabel('Rotation [°]')
    plt.ylabel(r'Deviation of relative intensity from expected value [unit less]')
    plt.grid()

    # Save the plot
    plt.savefig(f'figures/plot-{timestamp}-c.svg')
    plt.show()
