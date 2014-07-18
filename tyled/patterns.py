import logging


def apply_pattern(img, tiles, pattern):
    pattern_funcs = {'grid': grid,
                    'hstripe': hstripe,
                    'vstripe': vstripe}
    return pattern_funcs[pattern](img, tiles)


def _make_grid(out, tiles, design):
    logging.debug('Arranging tiles in {0} layout'.format(design))
    cnt = 0
    for x in range(0, out.size[0], tiles[0].size[0]):
        if design == 'grid' or design == 'vstripe':
            cnt += 1
        elif design == 'hstripe':
            cnt = 0
        for y in range(0, out.size[1], tiles[0].size[1]):
            if design == 'grid' or design == 'hstripe':
                cnt += 1
            logging.debug('Placing tile at ({0}, {1})'.format(x, y))
            out.paste(tiles[cnt % len(tiles)], (x, y))

    return out


def grid(out, tiles):
    return _make_grid(out, tiles, 'grid')


def hstripe(out, tiles):
    return _make_grid(out, tiles, 'hstripe')


def vstripe(out, tiles):
    return _make_grid(out, tiles, 'vstripe')
