tyled
=====

A lightweight image tiler written in Python.


We all like tiling window manager (hopefully...) so why not tiled images to go with them?

Requirements
=====

* [Pillow](https://pypi.python.org/pypi/Pillow)
* [Python 3](https://www.python.org/)


Installation
=====
Tyled has a setup.py that makes installation easy. Open a terminal, change to the directory that tyled is in and enter the following:

```
sudo python setup.py install
```

Usage
=====

* **-t / --tile:** A comma separated list of image files that should be tiled. This image must be no larger than 40x40 (else a thumbnail will be automatically generated)

* **-o / --out:** The filename that the generated image will be saved to.

* **-bg / --background:** The background colour of the generated image. If there is any areas of alpha in the tile, this colour will show through.

* **-w / --width:** The width of the generated image.

* **-h / --height:** The height of the generated image.

* **-of / --out-filters:** The filters to be applied to the output image, after the tiles have been placed. Filters should be supplied as a comma separated list. Each filter can be run multiple times to increase its effect. To do this, supply an integer after the filter name, such as:

```
blur:5
```

Possible filters can be seen [here](http://pillow.readthedocs.org/en/latest/reference/ImageFilter.html#filters).

* **-tf / --tile-filters:** The filters to be applied to the tile image, before being places. Filters should be supplied as a comma separated list. Each filter can be run multiple times to increase its effect. To do this, supply an integer after the filter name, such as:

```
blur:5
```

Possible filters can be seen [here](http://pillow.readthedocs.org/en/latest/reference/ImageFilter.html#filters).

* **-sh / --show:** When set, the generated image will be displayed upon completion.

* **-v / --verbose:** Whether or not to display extra information during processing.

* **-e / --effects:** The effects to be applied to the generated image and the order in which they should be applied. Effects are separated by commas and the arguments passed to effects are separated by colons.

* **-s / --size:** The size of the generated tile. Should be in the form WidthxHeight.

* **-xc / --xcolours:** A path to a .Xresources or .Xdefaults file. The colours contained in the file will be used as the colour palette for generating tiles. **This option can't be used with -t or -c.**

* **-c / --colours:** A comma separated list of colours in the format #RRGGBB. Each colour will be converted into a tile. **This option can't be used with -xc or -t.**

* **-p / --pattern:** The pattern to arrange the tiles in. Possible values can be seen [here](#Patterns)

Effects
=====

* [Brightness](#brightness)
* [Resize](#resize)

### Brightness
Change the brightness of the image. A value of 1 causes no change. Less than one causes the image to be darkened and a value greater than 1 causes the image to be lightened.

```
-e brightness:1
```

### Resize
Resize the final image by the scale factor passed as an argument. 1 will cause no change.

```
-e resize:4
```

Patterns
=====

* **Grid:** Arrange the tiles in a grid format.

```
-p grid
```

* **Vertical Stripe:** Display the tiles in a vertical stripe format.

```
-p vstripe
```

* **Horizontal Stripe:** Display the tiles in a horizontal stripe format.

```
-p hstripe
```
