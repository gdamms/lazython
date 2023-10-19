import sys
import re
import termios
import os


class Renderer:
    """The renderer.

    This class is used to render the screen. It is not meant to be instantiated.
    """

    class R:
        def start(self):
            sys.stdout.write('\x1b[?1049h')  # Save screen.
            sys.stdout.write('\x1b[?25l')  # Hide cursor.
            sys.stdout.flush()

        def stop(self):
            sys.stdout.write('\x1b[?1049l')  # Restore screen.
            sys.stdout.write('\x1b[?25h')  # Show cursor.
            sys.stdout.flush()

        def __del__(self):
            self.stop()

    INSTANCE: 'R' = R()
    BUFFER: str = ''


def start() -> None:
    """Start the renderer."""
    Renderer.INSTANCE.start()


def stop() -> None:
    """Stop the renderer."""
    Renderer.INSTANCE.stop()


def refresh() -> None:
    """Refresh the screen."""
    sys.stdout.write(Renderer.BUFFER)
    sys.stdout.flush()
    Renderer.BUFFER = ''


def clear() -> None:
    """Clear the screen."""
    Renderer.BUFFER += f'\x1b[2J'


def get_cursor_pos() -> tuple[int, int]:
    """Get the cursor position.

    Returns:
        tuple[int, int]: The cursor position.
    """
    # Init settings.
    old_stdin_mode = termios.tcgetattr(sys.stdin)
    new_stdin_mode = termios.tcgetattr(sys.stdin)
    new_stdin_mode[3] = new_stdin_mode[3] & ~(termios.ECHO | termios.ICANON)
    termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, new_stdin_mode)

    # Request cursor position.
    sys.stdout.write('\x1b[6n')
    sys.stdout.flush()

    # Read response.
    val = ""
    while not (val := val + sys.stdin.read(1)).endswith('R'):
        continue

    # Restore settings.
    termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, old_stdin_mode)

    # Parse response.
    val = re.match(r'\x1b\[(\d+);(\d+)R', val).groups()
    return int(val[1]) - 1, int(val[0]) - 1


def goto(x: int, y: int) -> None:
    """Go to the specified position.

    Args:
        x (int): The x.
        y (int): The y.
    """
    Renderer.BUFFER += f'\x1b[{y+1};{x+1}H'


TAB_WIDTH = 4

COLOR_EXPR = r'\x1b\[[0-9;]*m'
SAVE_EXPR = r'\x1b7'
RESTORE_EXPR = r'\x1b8'
GOTO_EXPR = r'\x1b\[\d+;\d+H'
RETURN_EXPR = r'\r'
NEWLINE_EXPR = r'\n'
TAB_EXPR = r'\t'
ERASE_END_OF_LINE_EXPR = r'\x1b\[K'

FULL_EXPR = f'({COLOR_EXPR}|{SAVE_EXPR}|{RESTORE_EXPR}|{GOTO_EXPR}|{RETURN_EXPR}|{NEWLINE_EXPR}|{TAB_EXPR}|{ERASE_END_OF_LINE_EXPR})'


def addstr(
        text: str,
        x: int = 0,
        y: int = 0,
        width: int = -1,
        height: int = -1,
        scroll: int = 0,
        no_draw: bool = False,
) -> tuple[int, int]:
    """Add a string to the screen.

    Args:
        text (str): The text.
        x (int, optional): The x. Defaults to 0.
        y (int, optional): The y. Defaults to 0.
        width (int, optional): The width. Defaults to -1. If -1, then the width is not limited.
        height (int, optional): The height. Defaults to -1. If -1, then the height is not limited.
        scroll (int, optional): The scroll. Defaults to 0.
        no_draw (bool, optional): If True, then the text will not be drawn. It is useful to get the number of lines and columns. Defaults to False.

    Returns:
        tuple[int, int]: The number of columns and the number of lines.
    """
    # Verify arguments.
    size = os.get_terminal_size()
    if width == -1:
        width = size.columns
    if height == -1:
        height = size.lines

    x = max(0, min(x, size.columns - 1))
    y = max(0, min(y, size.lines - 1))
    width = max(0, min(width, size.columns - x))
    height = max(0, min(height, size.lines - y))

    # Init.
    cursor_x = 0
    cursor_y = -scroll
    saved_cursor_x = 0
    saved_cursor_y = 0
    goto(x + cursor_x, y + cursor_y)

    # Init line count.
    buffer_backup = Renderer.BUFFER
    cursor_min_x = cursor_x
    cursor_max_x = cursor_x
    cursor_min_y = cursor_y
    cursor_max_y = cursor_y

    strings = re.split(FULL_EXPR, text)
    for i, string in enumerate(strings):
        if i % 2 == 0:
            # Normal string.
            for char in string:
                if cursor_x >= width:
                    # Wrap.
                    cursor_x = 0
                    cursor_y += 1
                    goto(x, y + cursor_y)
                if 0 <= cursor_y < height:
                    Renderer.BUFFER += char
                cursor_x += 1
        else:
            # Escape sequence.
            if re.match(COLOR_EXPR, string):
                Renderer.BUFFER += string
            elif re.match(SAVE_EXPR, string):
                Renderer.BUFFER += string
                saved_cursor_x, saved_cursor_y = get_cursor_pos()
                saved_cursor_x -= x
                saved_cursor_y -= y
            elif re.match(RESTORE_EXPR, string):
                Renderer.BUFFER += string
                goto(x + saved_cursor_x, y + saved_cursor_y)
                cursor_x = saved_cursor_x
                cursor_y = saved_cursor_y - scroll
            elif re.match(GOTO_EXPR, string):
                cursor_x, cursor_y = re.match(GOTO_EXPR, string).groups()
                cursor_x = int(cursor_x) - 1
                cursor_y = int(cursor_y) - 1 - scroll
                goto(x + cursor_x, y + cursor_y)
            elif re.match(RETURN_EXPR, string):
                cursor_x = 0
                goto(x, y + cursor_y)
            elif re.match(NEWLINE_EXPR, string):
                cursor_x = 0
                cursor_y += 1
                goto(x, y + cursor_y)
            elif re.match(TAB_EXPR, string):
                cursor_x += TAB_WIDTH - cursor_x % TAB_WIDTH
                if cursor_x >= width:
                    # Wrap.
                    cursor_x = 0
                    cursor_y += 1
                    goto(x, y + cursor_y)
            elif re.match(ERASE_END_OF_LINE_EXPR, string):
                Renderer.BUFFER += ' ' * (width - cursor_x)
                goto(x + cursor_x, y + cursor_y)
            else:
                raise Exception('Invalid escape sequence.')

        # Update cursor min and max y.
        if cursor_x < cursor_min_x:
            cursor_min_x = cursor_x
        if cursor_x > cursor_max_x:
            cursor_max_x = cursor_x
        if cursor_y < cursor_min_y:
            cursor_min_y = cursor_y
        if cursor_y > cursor_max_y:
            cursor_max_y = cursor_y

    # Restore buffer.
    if no_draw:
        Renderer.BUFFER = buffer_backup

    return cursor_max_x - cursor_min_x, cursor_max_y - cursor_min_y
