#!/usr/bin/env python3
import argparse
from PIL import Image, ImageFilter

class ImageNotSquare(Exception):
    pass

class TileNotAFactor(Exception):
    pass

def main(args):
    tile = Image.open(args.tile)
    out = Image.new('RGBA', (args.width, args.height), args.background)

    if tile.size[0] != tile.size[1]:
        raise ImageNotSquare('Image size is {0} x {1}'.format(*tile.size))

    if tile.size[0] > 40:
        print('Warning, tile image is larger than 40x40, making it into a thumbnail')
        tile.thumbnail((40, 40))

    if out.size[0] % tile.size[0] is not 0 or out.size[1] % tile.size[1] is not 0:
        raise TileNotAFactor('Tile of size {0} x {1} doesn\'t fit perfectly in {2} x {3}'.format(*(tile.size + out.size)))

    for x in range(0, out.size[0], tile.size[0]):
        for y in range(0, out.size[1], tile.size[1]):
            if args.verbose:
                print('Placing tile at ({0}, {1})'.format(x, y))
            out.paste(tile, (x, y))

    if args.filters:
        if args.verbose:
            print("Applying filters {0}".format(args.filters))
        out = apply_filters(out, args.filters)

    out.save(args.out)

    if args.show:
        out.show()

def apply_filters(img, filters):

    filter_funcs = {'blur': ImageFilter.BLUR,
            'contour': ImageFilter.CONTOUR,
            'detail': ImageFilter.DETAIL,
            'edge_enhance': ImageFilter.EDGE_ENHANCE,
            'edge_enhance_more': ImageFilter.EDGE_ENHANCE_MORE,
            'emboss': ImageFilter.EMBOSS,
            'find_edges': ImageFilter.FIND_EDGES,
            'smooth': ImageFilter.SMOOTH,
            'smooth_more': ImageFilter.SMOOTH_MORE,
            'sharpen': ImageFilter.SHARPEN}

    for filter in filters:
        img = img.filter(filter_funcs[filter])

    return img


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=
                                'A lightweight image tiler written in Python.',
                                conflict_handler='resolve')
    parser.add_argument('-t', '--tile', type=str, help='The image to be tiled',
            required=True)
    parser.add_argument('-o', '--out', type=str, help='The name of the image used as output',
            required=True)
    parser.add_argument('-bg', '--background', type=str, default='#000000',
            help='The background colour that will be displayed where the tile has alpha')
    parser.add_argument('-w', '--width', type=int, required=True)
    parser.add_argument('-h', '--height', type=int, required=True)
    parser.add_argument('-f', '--filters', action='append')
    parser.add_argument('-s', '--show', action='store_true',
            help='Show the image upon completion')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()
    main(args)

