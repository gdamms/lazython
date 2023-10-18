import termios
import sys
import os
import select


def get_key(timeout: float = None) -> int:
    """Get a key from stdin.

    Args:
        timeout (float, optional): The timeout in seconds. Defaults to None. If None, then the function will block until a key is pressed.

    Returns:
        int: The key code.
    """
    try:
        # Init settings.
        old_settings = termios.tcgetattr(sys.stdin)
        new_settings = termios.tcgetattr(sys.stdin)
        new_settings[3] = new_settings[3] & ~(termios.ECHO | termios.ICANON)  # lflags
        new_settings[6][termios.VMIN] = 0  # cc
        new_settings[6][termios.VTIME] = 0  # cc
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, new_settings)

        # Read.
        r, _, _ = select.select([sys.stdin], [], [], timeout)
        key = None
        if r:
            ch_set = []
            ch = os.read(sys.stdin.fileno(), 1)
            while ch is not None and len(ch) > 0:
                ch_set.append(ch[0])
                ch = os.read(sys.stdin.fileno(), 1)
            key = ch_set

        # Restore settings.
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

        if key is None:
            return None

        # Convert to int.
        val = 0
        for i, ch in enumerate(key):
            val += ch << (8 * i)

        return val

    except KeyboardInterrupt:
        return 0


if __name__ == '__main__':
    print('Press any key to get its code. Press Ctrl+C to exit.')
    while True:
        key = get_key()
        if key is not None:
            print('Key code:', key)
        if key == 0:
            break
