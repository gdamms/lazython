import re


class rstr(str):
    """A string that can be rendered on the screen.

    It is used to manipulate strings that contain ANSI escape sequences as if they were rendered on the screen.
    """

    __EXPR = r'(\x1b\[[0-9;]*m)'

    def __init__(self: 'rstr', text: str) -> None:
        """Constructor.

        Args:
            text (str): The text.
        """
        self.__raw_text = re.sub(rstr.__EXPR, '', text)

        split = re.split(rstr.__EXPR, text)
        split.insert(0, '\x1b8')
        self.__vals = [(split[i], split[i + 1]) for i in range(0, len(split), 2)]

    def __len__(self) -> int:
        """Get the length of the text after it is rendered.

        Returns:
            int: The length of the text after it is rendered.
        """
        return self.__raw_text.__len__()

    def __getitem__(self: 'rstr', key: int | slice) -> str:
        """Get the character at the specified index.

        Args:
            key (int, slice): The index.

        Returns:
            str: The character at the specified index.
        """
        if isinstance(key, int):
            # Validate the index.
            if key < 0:
                key += len(self)
            if key < 0:
                raise IndexError('Index out of range')
            if key >= len(self):
                raise IndexError('Index out of range')

            cur = 0
            for val in self.__vals:
                if cur <= key < cur + len(val[1]):
                    return f'\x1b7{val[0]}{val[1][key - cur]}\x1b8'
                cur += len(val[1])

        elif isinstance(key, slice):
            # TODO: Validate the slice.
            # TODO: Implement complex slices (step != 1, negative start or stop, etc.).
            res = '\x1b7'
            cur = 0
            started = False
            key_start = key.start or 0
            key_stop = min((key.stop or len(self)), len(self))
            for val in self.__vals:
                # Add first substring.
                if cur <= key_start < cur + len(val[1]) and not started:
                    start_val = key_start - cur
                    res += val[0] + val[1][start_val:]
                    started = True
                # Add middle substrings.
                elif started:
                    res += val[0] + val[1]
                # Add last substring.
                if cur <= key_stop <= cur + len(val[1]):
                    end_val = cur + len(val[1]) - key_stop
                    res = res[:len(res)-end_val] + '\x1b8'
                    return rstr(res)
                cur += len(val[1])


if __name__ == '__main__':
    raise RuntimeError('This module is not meant to be ran by the user')
