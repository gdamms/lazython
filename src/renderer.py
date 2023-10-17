import sys
import re

from rstr import rstr


class Renderer:
    """The renderer.

    This class is used to render the screen. It is not meant to be instantiated.
    """

    class R:
        def __init__(self):
            sys.stdout.write('\x1b[?1049h')
            sys.stdout.write('\x1b[?25l')
            sys.stdout.flush()

        def __del__(self):
            sys.stdout.write('\x1b[?1049l')
            sys.stdout.write('\x1b[?25h')
            sys.stdout.flush()

    INSTANCE: 'R' = R()
    BUFFER: str = ''


def addstr(y: int, x: int, text: str) -> None:
    """Add a string to the screen.

    Args:
        y (int): The y.
        x (int): The x.
        text (str): The text.
    """
    expr = r'(\x1b[78])'
    split = re.split(expr, text)
    cur = 0
    for i, val in enumerate(split):
        if i % 2 == 0:
            Renderer.BUFFER += f'\033[{y+1};{x+cur+1}H{val}'
            rval = rstr(val)
            cur += len(rval)
        else:
            Renderer.BUFFER += val


def refresh() -> None:
    """Refresh the screen."""
    sys.stdout.write(Renderer.BUFFER)
    sys.stdout.flush()
    Renderer.BUFFER = ''


def clear() -> None:
    """Clear the screen."""
    Renderer.BUFFER += f'\x1b[2J'
