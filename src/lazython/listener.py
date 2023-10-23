import select
import sys
import termios
import os
import re
from typing import *


class Listener:
    def __init__(self: 'Listener'):
        """Constructor."""
        self.listening = False

        self.old_settings = None

        self.key_callbacks = []
        self.click_callbacks = []

    def prepare(self: 'Listener'):
        """Prepare to listen."""
        # Init settings.
        self.old_settings = termios.tcgetattr(sys.stdin)
        new_settings = termios.tcgetattr(sys.stdin)
        new_settings[3] = new_settings[3] & ~(termios.ECHO | termios.ICANON)  # lflags
        new_settings[6][termios.VMIN] = 0  # cc
        new_settings[6][termios.VTIME] = 0  # cc
        termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, new_settings)

        # Send ANSI escape sequences.
        sys.stdout.write('\x1b[?1000h')  # Record mouse events.
        sys.stdout.flush()

    def terminate(self: 'Listener'):
        """Terminate listening."""
        # Send ANSI escape sequences.
        sys.stdout.write('\x1b[?1000l')  # Stop recording mouse events.
        sys.stdout.flush()

        # Restore settings.
        termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, self.old_settings)

    def add_key_callback(self: 'Listener', callback: 'Callable[[int], None]'):
        """Add a key callback.

        Args:
            callback (Callable[[int], None]): The callback to add.

        The callback will be called with the key as an int.
        """
        self.key_callbacks.append(callback)

    def add_click_callback(self: 'Listener', callback: 'Callable[[int, int, int], None]'):
        """Add a click callback.

        Args:
            callback (Callable[[int, int, int], None]): The callback to add.

        The callback will be called with the key, x and y as ints.
        """
        self.click_callbacks.append(callback)

    def stop(self: 'Listener'):
        """Stop listening."""
        self.listening = False

    def listen(self: 'Listener'):
        """Listen to events."""
        if self.listening:
            raise Exception('Already listening.')

        self.prepare()

        self.listening = True
        while self.listening:
            try:
                # Read.
                r, _, _ = select.select([sys.stdin], [], [])
                if r:
                    ch_set = []
                    ch = os.read(sys.stdin.fileno(), 1)
                    while ch is not None and len(ch) > 0:
                        ch_set.append(ch)
                        ch = os.read(sys.stdin.fileno(), 1)
                    key = ch_set

                    # Click callback.
                    click_expr = r'\x1b\[M(.)(.)(.)'
                    if match := re.match(click_expr, str(key)):
                        key, x, y = match.groups()
                        key, x, y = ord(key), ord(x), ord(y)
                        key = key - 32
                        x = x - 32 if x < 128 else x - 56448 + 128 - 32
                        y = y - 32 if y < 128 else y - 56448 + 128 - 32
                        for callback in self.click_callbacks:
                            callback(key, x, y)
                        continue

                    # Convert to int.
                    val = 0
                    for i, ch in enumerate(key):
                        val += ord(ch) << (8 * i)

                    # Key callback.
                    for callback in self.key_callbacks:
                        callback(val)

            except KeyboardInterrupt:
                # Key callback.
                val = 0
                for callback in self.key_callbacks:
                    callback(val)

        self.terminate()
