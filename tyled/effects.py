def apply_effects(img, effects):
    effect_funcs = {'brightness': change_brightness}
    for e in effects:
        eff, args = _parse_effect(e)
        img = effect_funcs[eff](img, *args)
    return img

def _parse_effect(effect):
    effect = effect.split(':')
    e, *args = effect
    return (e, args)

def change_brightness(img, amount):
    img = img.point(lambda x: x * float(amount))
    return img
