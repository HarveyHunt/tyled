#!/usr/bin/env python3
import argparse
import logging
from PIL import Image
from tyled.effects import apply_effects, apply_filters


def main(args):
    tile = Image.open(args.tile).convert('RGBA')
    out = Image.new('RGBA', (args.width, args.height), args.background)

    check_tile(tile)
    if out.size[0] % tile.size[0] or out.size[1] % tile.size[1]:
        logging.warn('Tile of size {0} x {1} doesn\'t fit perfectly'
               ' in {2} x {3}'.format(*(tile.size + out.size)))

    if args.tile_filters:
        tile = apply_filters(tile, args.tile_filters.split(','))

    make_grid(out, tile, args.verbose)
    if args.out_filters:
        out = apply_filters(out, args.out_filters.split(','))

    if args.effects:
        out = apply_effects(out, args.effects.split(','))

    out.save(args.out)

    if args.show:
        out.show()


def check_tile(tile):
    if tile.size[0] > 40:
        logging.warn('Tile image is larger than 40x40, making it into a thumbnail')
        tile.thumbnail((40, 40))


def make_grid(out, tile, verbose):
    for x in range(0, out.size[0], tile.size[0]):
        for y in range(0, out.size[1], tile.size[1]):
            logging.debug('Placing tile at ({0}, {1})'.format(x, y))
            out.paste(tile, (x, y))


def init():
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
    'separated list of filters to be applied to the output image. Args are colon '
    'separated and dictate how many times to apply the filter.')
    parser.add_argument('-tf', '--tile-filters', type=str, help='A comma '
    'separated list of filters to be applied to the tile image. Args are colon '
    'separated and dictate how many times to apply the filter.')
    parser.add_argument('-e', '--effects', type=str, help='A comma '
    'separated list of effects to be applied to the output image. Args are'
    'colon separated e.g. effect_foo:1:2:3')
    parser.add_argument('-s', '--show', action='store_true',
            help='Show the image upon completion')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARN)

    main(args)


if __name__ == '__main__':
    init()
