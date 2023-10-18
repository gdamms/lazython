class Box:
    def __init__(
            self: 'Box',
            width: int,
            height: int,
            x: int = 0,
            y: int = 0,
    ) -> None:
        """Initialize a box.

        Args:
            width (int): The width of the box.
            height (int): The height of the box.
            x (int, optional): The x of the box. Defaults to 0.
            y (int, optional): The y of the box. Defaults to 0.
        """
        self.__width = width
        self.__height = height
        self.__x = x
        self.__y = y

    # Getters.

    def get_width(
            self: 'Box',
    ) -> int:
        """Get the width. (Including the border.)"""
        return self.__width

    def get_height(
            self: 'Box',
    ) -> int:
        """Get the height. (Including the border.)"""
        return self.__height

    def get_x(
            self: 'Box',
    ) -> int:
        """Get the x. (Including the border.)"""
        return self.__x

    def get_y(
            self: 'Box',
    ) -> int:
        """Get the y. (Including the border.)"""
        return self.__y

    # Setters.

    def set_width(
            self: 'Box',
            width: int,
    ) -> None:
        """Set the width. (Including the border.)"""
        self.__width = width

    def set_height(
            self: 'Box',
            height: int,
    ) -> None:
        """Set the height. (Including the border.)"""
        self.__height = height

    def set_x(
            self: 'Box',
            x: int,
    ) -> None:
        """Set the x. (Including the border.)"""
        self.__x = x

    def set_y(
            self: 'Box',
            y: int,
    ) -> None:
        """Set the y. (Including the border.)"""
        self.__y = y
