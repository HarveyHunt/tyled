tyled
=====

A lightweight image tiler written in Python.


We all like tiling window manager (hopefully...) so why not tiled images to go with them?

Requirements
=====

* [Pillow](https://pypi.python.org/pypi/Pillow)
* [Python 3](https://www.python.org/)

Usage
=====

* **-t / --tile:** The filename of the image to be tiled. This image must be no larger than 40x40 (else a thumbnail will be automatically generated)

* **-o / --out:** The filename that the generated image will be saved to.

* **-bg / --background:** The background colour of the generated image. If there is any areas of alpha in the tile, this colour will show through.

* **-w / --width:** The width of the generated image.

* **-h / --height:** The height of the generated image.

* **-of / --out-filters:** The filters to be applied to the output image, after the tiles have been placed. Filters should be supplied as a comma separated list. Possible filters can be seen [here](http://pillow.readthedocs.org/en/latest/reference/ImageFilter.html#filters).

* **-tf / --tile-filters:** The filters to be applied to the tile image, before being places. Filters should be supplied as a comma separated list. Possible filters can be seen [here](http://pillow.readthedocs.org/en/latest/reference/ImageFilter.html#filters).

* **-s / --show:** When set, the generated image will be displayed upon completion.

* **-v / --verbose:** Whether or not to display extra information during processing.

* **-e / --effects:** The effects to be applied to the generated image and the order in which they should be applied. Effects are separated by commas and the arguments passed to effects are separated by colons.

Effects
=====

* [Brightness](#brightness)

## Brightness
Change the brightness of the image. A value of 1 causes no change. Less than one causes the image to be darkened and a value greater than 1 causes the image to be lightened.

```
-e brightness:1
```

