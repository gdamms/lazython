

class Line:
    """The line class.

    Not that useful, but to stay organized.
    """

    __ID: int = 0

    def __init__(
            self: 'Line',
            text: str = '',
            subtexts: list[str] = [],
    ) -> None:
        self.__text = text
        self.__subtexts = subtexts
        self.__scroll = [-1 for _ in range(len(subtexts))]

        self.__id = Line.__ID
        Line.__ID += 1

    def get_text(
            self: 'Line',
    ) -> str:
        """Get the text.

        Returns:
            str: The text.
        """
        return self.__text

    def set_text(
            self: 'Line',
            text: str,
    ) -> None:
        """Set the text.

        Args:
            text (str): The text.
        """
        self.__text = text

    def get_subtext(
            self: 'Line',
            subtab: int,
    ) -> str:
        """Get the subtext at the specified subtab.

        Args:
            subtab (int): The subtab.

        Returns:
            str: The subtext at the specified subtab.
        """
        return self.__subtexts[subtab] if subtab < len(self.__subtexts) else ''

    def set_subtext(
            self: 'Line',
            subtab: int,
            subtext: str,
    ) -> None:
        """Set the subtext at the specified subtab.

        Args:
            subtab (int): The subtab.
            subtext (str): The subtext.
        """
        if subtab < len(self.__subtexts):
            self.__subtexts[subtab] = subtext
        else:
            self.__subtexts += [''] * (subtab - len(self.__subtexts)) + [subtext]
            self.__scroll += [-1] * (subtab - len(self.__scroll) + 1)

    def get_subtexts(
            self: 'Line',
    ) -> list[str]:
        """Get the subtexts.

        Returns:
            list[str]: The subtexts.
        """
        return self.__subtexts

    def set_subtexts(
            self: 'Line',
            subtexts: list[str],
    ) -> None:
        """Set the subtexts.

        Args:
            subtexts (list[str]): The subtexts.
        """
        self.__subtexts = subtexts

    def get_nb_subtext(
            self: 'Line',
    ) -> int:
        """Get the number of subtexts.

        Returns:
            int: The number of subtexts.
        """
        return len(self.__subtexts)

    def get_scroll(
            self: 'Line',
            subtab: int,
    ) -> int:
        """Get the scroll at the specified subtab.

        Args:
            subtab (int): The subtab.

        Returns:
            int: The scroll at the specified subtab.
        """
        return self.__scroll[subtab] if subtab < len(self.__scroll) else -1

    def set_scroll(
            self: 'Line',
            subtab: int,
            scroll: int,
    ) -> None:
        """Set the scroll at the specified subtab.

        Args:
            subtab (int): The subtab.
            scroll (int): The scroll.
        """
        if subtab < len(self.__scroll):
            self.__scroll[subtab] = scroll
        else:
            self.__scroll += [-1] * (subtab - len(self.__scroll)) + [scroll]
