import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from datetime import datetime

from settings import entries

figure, axis = plt.subplots(len(entries), 2, tight_layout=True)

rotations = np.empty((len(entries), 1))
rotations_err = np.empty((len(entries), 1))
intensities = np.empty((len(entries), 1))
intensities_err = np.empty((len(entries), 1))

timestamp = datetime.now().strftime('%d-%m@%H-%M-%S')

for i in range(len(entries)):
    entry = entries[i]

    file_name = entry[0]
    rotation = entry[1]
    rotation_error = entry[2]

    image = Image.open(file_name)

    print(f'Processing image: {file_name}, has dimensions: {image.size}')

    intensity = np.max(np.asarray(image), 2)

    axis[i, 0].imshow(image)
    axis[i, 0].set_title(file_name)

    axis[i, 1].imshow(intensity, cmap='gray')
    axis[i, 1].set_title(f'{file_name} intensity')

    rotations[i] = rotation
    rotations_err[i] = rotation_error
    intensities[i] = np.mean(intensity)
    intensities_err[i] = np.std(intensity)

    print(
        f'Average intensity: {np.mean(intensity):.1e}±{np.std(intensity):.0e} for rotation: {rotation:.1e}±{rotation_error:.0e}°')

relative_intensities = intensities / np.max(intensities)
relative_intensities_err = (1 / np.max(intensities)) * np.sqrt(
    np.square(intensities_err) + np.square(intensities_err[np.argmax(intensities)]) / np.square(
        intensities[np.argmax(intensities)]))

plt.savefig(f'figures/maps-{timestamp}.svg')
plt.show()

plt.title('Intensity vs. rotation')
plt.grid()
plt.errorbar(rotations, relative_intensities, relative_intensities_err, rotations_err)
plt.xlabel('Rotation [°]')
plt.ylabel(r'Intensity ($I/I_0$) [unit less]')

plt.savefig(f'figures/plot-{timestamp}.svg')
plt.show()
