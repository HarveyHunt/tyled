#!/usr/bin/env python3
import argparse
import logging
from PIL import Image, ImageFilter


class ImageNotSquare(Exception):
    pass


class TileNotAFactor(Exception):
    pass


def main(args):
    tile = Image.open(args.tile).convert('RGBA')
    out = Image.new('RGBA', (args.width, args.height), args.background)

    check_tile(tile)
    if out.size[0] % tile.size[0] is not 0:
        raise TileNotAFactor('Tile of size {0} x {1} doesn\'t fit perfectly'
               ' in {2} x {3}'.format(*(tile.size + out.size)))

    if args.tile_filters:
        tile = apply_filters(tile, args.tile_filters.split(','))

    make_grid(out, tile, args.verbose)
    if args.out_filters:
        out = apply_filters(out, args.out_filters.split(','))
    out.save(args.out)

    if args.show:
        out.show()


def check_tile(tile):
    if tile.size[0] != tile.size[1]:
        raise ImageNotSquare('Image size is {0} x {1}'.format(*tile.size))

    if tile.size[0] > 40:
        logger.warn('Tile image is larger than 40x40, making it into a thumbnail')
        tile.thumbnail((40, 40))


def make_grid(out, tile, verbose):
    for x in range(0, out.size[0], tile.size[0]):
        for y in range(0, out.size[1], tile.size[1]):
            logger.debug('Placing tile at ({0}, {1})'.format(x, y))
            out.paste(tile, (x, y))


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
        logger.debug("Applying filters {0} to {1}".format(filter, img))
        img = img.filter(filter_funcs[filter])

    return img


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A lightweight image tiler written in Python.',
                                    conflict_handler='resolve')
    parser.add_argument('-t', '--tile', type=str, help='The image to be tiled',
                        required=True)
    parser.add_argument('-o', '--out', type=str, help='The name of the image used as output',
                        required=True)
    parser.add_argument('-bg', '--background', type=str, default='#000000',
            help='The background colour that will be displayed where the tile has alpha')
    parser.add_argument('-w', '--width', type=int, required=True)
    parser.add_argument('-h', '--height', type=int, required=True)
    parser.add_argument('-of', '--out-filters', type=str, help='A comma '
    'separated list of filters to be applied to the output image')
    parser.add_argument('-tf', '--tile-filters', type=str, help='A comma '
    'separated list of filters to be applied to the tile image')
    parser.add_argument('-s', '--show', action='store_true',
            help='Show the image upon completion')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG if args.verbose else logging.WARN)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG if args.verbose else logging.WARN)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    main(args)
