import logging

def apply_pattern(img, tiles, pattern):
    pattern_funcs = {'grid': make_grid}
    return pattern_funcs[pattern](img, tiles)


def make_grid(out, tiles):
    tile = tiles[0]
    for x in range(0, out.size[0], tile.size[0]):
        for y in range(0, out.size[1], tile.size[1]):
            logging.debug('Placing tile at ({0}, {1})'.format(x, y))
            out.paste(tile, (x, y))

    return out
