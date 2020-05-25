# Analysis software for EN6
This software has been written to analyse image data for my EN6 experiment
. The main file is `analysis.py` which handles all the logic. The file
 `settings.py` should contain specifications as to what should be analysed. 

## Main functionality
Given a series of images with their respective rotation the software will
determine the average intensity of each image and map that value between 0
and 1 where 1 is maximum brightness and 0 minimum brightness. It has the
ability to create an intensity map and will generate a plot of intensity
of angle. It is also able to compare it to the expected cosine squared
pattern.

## Example `settings.py`
```python
create_map = False
map_values = True
compare = True

entries = [
    # file name, rotation, error
    ('data/image1.TIFF', 13, 3),
    ('data/image2.TIFF', 50, 3)
]
```
All angles should be given in degrees not radians.
