from rstr import rstr


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
        self.__text = rstr(text)
        self.__subtexts = [rstr(subtext) for subtext in subtexts]

        self.__id = Line.__ID
        Line.__ID += 1

    def get_line_line(
            self: 'Line',
    ) -> str:
        """Get the line line.

        Returns:
            str: The line line.

        Basically, the line line is the first line of the text.
        """
        return self.__text.split('\n')[0]

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

    def get_nb_subtext(
            self: 'Line',
    ) -> int:
        """Get the number of subtexts.

        Returns:
            int: The number of subtexts.
        """
        return len(self.__subtexts)