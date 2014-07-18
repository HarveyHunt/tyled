import logging
from PIL import ImageFilter


def apply_effects(img, effects):
    effects = effects.split(',')

    effect_funcs = {'brightness': eff_brightness}
    for e in effects:
        eff, args = _parse_args(e)
        logging.debug('Applying effect {0} with args {1} to {2}'.format(
            eff, args, img))
        img = effect_funcs[eff](img, *args)
    return img


def _parse_args(effect):
    effect = effect.split(':')
    e, *args = effect
    return (e, args)


def eff_brightness(img, amount):
    return img.point(lambda x: x * float(amount))


def apply_filters(imgs, filters):
    filters = filters.split(',')

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

    for img in imgs:
        for f in filters:
            filter, count = _parse_args(f)
            for i in range(int(count[0])):
                logging.debug("Applying filter {0} to {1}".format(filter, img))
                imgs.append(img.filter(filter_funcs[filter]))

    return imgs
