#!/usr/bin/env python3
import argparse
import re
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
            logging.debug('Opened tile {0}'.format(tile))
            check_tile(tile)
            tiles.append(tile)

    elif args.xcolours:
        colours = parse_xresources(args.xcolours)
        tiles = generate_tiles(colours, args.size)
    elif args.colours:
        colours = args.colours.split(',')
        tiles = generate_tiles(colours, args.size)
    else:
        raise ValueError('No list of tiles or colour information have been inputted')

    if args.tile_filters:
        tiles = apply_filters(tiles, args.tile_filters)

    out = apply_pattern(out, tiles, args.pattern)

    if args.out_filters:
        out = apply_filters(out, args.out_filters)

    if args.effects:
        out = apply_effects(out, args.effects)

    out.save(args.out)

    if args.show:
        out.show()


def generate_tiles(colours, size):
    size = tuple([int(x) for x in size.lower().split('x')])
    tiles = []
    for colour in colours:
        tiles.append(Image.new('RGBA', size, colour))
        logging.debug('Generated tile with colour {0}'.format(colour))
    return tiles


def parse_xresources(filename):
    colours = []
    colour_re = re.compile('.*?(color[^:]+|foreground|background):\s*(#[\da-z]{6})')
    with open(filename, 'r') as xc:
        for line in xc.readlines():
            if line.startswith('!'):
                continue
            match = colour_re.search(line.lower())
            if match:
                _, colour = match.groups()
                logging.debug('Found colour {0} in file {1}'.format(colour, filename))
                colours.append(colour)

    return colours


def check_tile(tile):
    if tile.size[0] > 40:
        logging.warn('Tile image is larger than 40x40, making it into a thumbnail')
        tile.thumbnail((40, 40))


def init():
    parser = argparse.ArgumentParser(description='A lightweight image tiler written in Python.',
                                    conflict_handler='resolve')
    parser.add_argument('-t', '--tiles', type=str, help='A comma separated list '
                    'of tile images')
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
    parser.add_argument('-sh', '--show', action='store_true',
            help='Show the image upon completion')
    parser.add_argument('-xc', '--xcolours', type=str, help='The path to the '
            'file which contains the xcolours to be used')
    parser.add_argument('-p', '--pattern', type=str, help='The pattern that '
            'the tile should be arranged in', default='grid')
    parser.add_argument('-c', '--colours', type=str, help='The colours that '
            'should be used for generating tiles.')
    parser.add_argument('-s', '--size', type=str, help='The size of the tiles that will be '
            'generated if colours are passed.', default='10x10')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    if args.xcolours and args.tiles:
        raise ValueError('Xcolours and tile image can\'t both be set')

    if args.xcolours and args.colours:
        raise ValueError('Xcolours and colours can\'t both be set')

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.WARN)

    main(args)


if __name__ == '__main__':
    init()
