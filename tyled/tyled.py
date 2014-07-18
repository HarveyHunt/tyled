#!/usr/bin/env python3
import argparse
import logging
from PIL import Image
from tyled.effects import apply_effects, apply_filters
from tyled.patterns import apply_pattern


def main(args):
    out = Image.new('RGBA', (args.width, args.height), args.background)

    tiles = []
    if args.tiles:
        for tile in args.tiles.split(','):
            tile = Image.open(tile).convert('RGBA')
            check_tile(tile)
            if out.size[0] % tile.size[0] or out.size[1] % tile.size[1]:
                logging.warn('Tile of size {0} x {1} doesn\'t fit perfectly'
                    ' in {2} x {3}'.format(*(tile.size + out.size)))
            tiles.append(tile)

    elif args.xcolours:
        colours = parse_colours(args.xcolours)
    else:
        raise ValueError('No list of tiles or colour information have been inputted')

    if args.tile_filters:
        tiles = apply_filters(tiles, args.tile_filters)

    out = apply_pattern(out, tiles, args.pattern)

    if args.out_filters:
        out = apply_filters(list(out), args.out_filters)

    if args.effects:
        out = apply_effects(out, args.effects)

    out.save(args.out)

    if args.show:
        out.show()


def parse_colours(filename):
    with open(filename, 'r') as xc:
        for line in xc.readlines():
            if line.startswith('!'):
                continue

def check_tile(tile):
    if tile.size[0] > 40:
        logging.warn('Tile image is larger than 40x40, making it into a thumbnail')
        tile.thumbnail((40, 40))


def init():
    parser = argparse.ArgumentParser(description='A lightweight image tiler written in Python.',
                                    conflict_handler='resolve')
    parser.add_argument('-t', '--tiles', type=str, help='A comma separated list '
                    'of tile images', required=True)
    parser.add_argument('-o', '--out', type=str, help='The name of the image used as output',
                        required=True)
    parser.add_argument('-bg', '--background', type=str, default='#000000',
            help='The background colour that will be displayed where the tile has alpha')
    parser.add_argument('-w', '--width', type=int, required=True)
    parser.add_argument('-h', '--height', type=int, required=True)
    parser.add_argument('-of', '--out-filters', type=str, help='A comma '
    'separated list of filters to be applied to the output image. Args are colon '
    'separated and dictate how many times to apply the filter')
    parser.add_argument('-tf', '--tile-filters', type=str, help='A comma '
    'separated list of filters to be applied to the tile image. Args are colon '
    'separated and dictate how many times to apply the filter')
    parser.add_argument('-e', '--effects', type=str, help='A comma '
    'separated list of effects to be applied to the output image. Args are'
    'colon separated e.g. effect_foo:1:2:3')
    parser.add_argument('-s', '--show', action='store_true',
            help='Show the image upon completion')
    parser.add_argument('-xc', '--xcolours', type=str, help='The path to the '
            'file which contains the xcolours to be used')
    parser.add_argument('-p', '--pattern', type=str, help='The pattern that '
            'the tile should be arranged in', default='grid')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    if args.xcolours and args.tile:
        raise argparse.ArgumentError('Xcolours and tile image can\'t both be set')

    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARN)

    main(args)


if __name__ == '__main__':
    init()
