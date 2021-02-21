"""
    weasyprint.svg.utils
    --------------------

    Util functions for SVG rendering.

"""

import re


UNITS = {
    'mm': 1 / 25.4,
    'cm': 1 / 2.54,
    'in': 1,
    'pt': 1 / 72,
    'pc': 1 / 6,
    'px': None,
}


def normalize(string):
    """Normalize a string corresponding to an array of various values."""
    string = string.replace('E', 'e')
    string = re.sub('(?<!e)-', ' -', string)
    string = re.sub('[ \n\r\t,]+', ' ', string)
    string = re.sub(r'(\.[0-9-]+)(?=\.)', r'\1 ', string)
    return string.strip()


def size(string, font_size=None, percentage_reference=None):
    if not string:
        return 0

    try:
        return float(string)
    except ValueError:
        # Not a float, try something else
        pass

    string = normalize(string).split(' ', 1)[0]
    if string.endswith('%'):
        assert percentage_reference is not None
        return float(string[:-1]) * percentage_reference / 100
    elif string.endswith('em'):
        assert font_size is not None
        return font_size * float(string[:-2])
    elif string.endswith('ex'):
        # Assume that 1em == 2ex
        assert font_size is not None
        return font_size * float(string[:-2]) / 2

    for unit, coefficient in UNITS.items():
        if string.endswith(unit):
            number = float(string[:-len(unit)])
            return number * (96 * coefficient if coefficient else 1)

    # Unknown size
    return 0
