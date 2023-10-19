from .line import Line
from .box import Box
from .renderer import addstr
from .vars import *


class Tab:
    """The tab class."""

    ID: int = 0

    def __init__(
            self: 'Tab',
            name: str = '',
            subtabs: list[str] = [],
            height_weight: float = 1,
            min_height: int = 1,
    ) -> None:
        # TODO: Check if the arguments are valid.
        self.__name = name
        self.__subtabs = subtabs

        self.__height_weight = height_weight  # The weight of the tab in the height calculation.
        self.__min_height = min_height  # The minimum height of the tab. It does not include the top and bottom lines.

        self.__lines: list[Line] = []

        self.__tab_box = Box(width=0, height=0, x=0, y=0)
        self.__content_box = Box(width=0, height=0, x=0, y=0)

        self.__selected_line = 0
        self.__selected_subtab = 0

        self.__tab_scroll = 0
        self.__content_scroll = 0

        self.__selected = False

        self.id = Tab.ID
        Tab.ID += 1

    def add_line(
            self: 'Tab',
            text: str = '',
            subtexts: list[str] = [],
    ) -> 'Line':
        """Add a line to the tab.

        Args:
            text (str, optional): The line text. Defaults to ''.
            subtexts (list[str], optional): The line contents. Defaults to [].

        Returns:
            Line: The line.

        The line text will be rendered on the tab.
        The line contents will be rendered on the content box, in the corresponding subtab.
        """
        new_line = Line(text=text, subtexts=subtexts)
        self.__lines.append(new_line)
        return new_line

    def clear_lines(
            self: 'Tab',
    ) -> None:
        """Clear the lines."""
        self.__lines = []

    def set_tab_width(
            self: 'Tab',
            width: int,
    ) -> None:
        """Set the tab width.

        Args:
            width (int): The tab width.
        """
        self.__tab_box.set_width(width)

    def set_tab_height(
            self: 'Tab',
            height: int,
    ) -> None:
        """Set the tab height.

        Args:
            height (int): The tab height.
        """
        self.__tab_box.set_height(height)

    def set_tab_x(
            self: 'Tab',
            x: int,
    ) -> None:
        """Set the tab x.

        Args:
            x (int): The tab x.
        """
        self.__tab_box.set_x(x)

    def set_tab_y(
            self: 'Tab',
            y: int,
    ) -> None:
        """Set the tab y.

        Args:
            y (int): The tab y.
        """
        self.__tab_box.set_y(y)

    def set_content_width(
            self: 'Tab',
            width: int,
    ) -> None:
        """Set the content width.

        Args:
            width (int): The content width.
        """
        self.__content_box.set_width(width)

    def set_content_height(
            self: 'Tab',
            height: int,
    ) -> None:
        """Set the content height.

        Args:
            height (int): The content height.
        """
        self.__content_box.set_height(height)

    def set_content_x(
            self: 'Tab',
            x: int,
    ) -> None:
        """Set the content x.

        Args:
            x (int): The content x.
        """
        self.__content_box.set_x(x)

    def set_content_y(
            self: 'Tab',
            y: int,
    ) -> None:
        """Set the content y.

        Args:
            y (int): The content y.
        """
        self.__content_box.set_y(y)

    def next_line(
            self: 'Tab',
    ) -> None:
        """Select the next line."""
        if len(self.__lines) == 0:
            return
        self.__selected_line += 1
        self.__selected_line %= len(self.__lines)
        self.__update_tab_scroll()
        self.__reset_content_scroll()

    def previous_line(
            self: 'Tab',
    ) -> None:
        """Select the previous line."""
        if len(self.__lines) == 0:
            return
        self.__selected_line -= 1
        self.__selected_line %= len(self.__lines)
        self.__update_tab_scroll()
        self.__reset_content_scroll()

    def next_subtab(
            self: 'Tab',
    ) -> None:
        """Select the next subtab."""
        if len(self.__subtabs) == 0:
            return
        self.__selected_subtab += 1
        self.__selected_subtab %= len(self.__subtabs)
        self.__reset_content_scroll()

    def previous_subtab(
            self: 'Tab',
    ) -> None:
        """Select the previous subtab."""
        if len(self.__subtabs) == 0:
            return
        self.__selected_subtab -= 1
        self.__selected_subtab %= len(self.__subtabs)
        self.__reset_content_scroll()

    def get_selected_line(
            self: 'Tab',
    ) -> 'Line':
        """Get the selected line.

        Returns:
            Line: The selected line.
        """
        return self.__lines[self.__selected_line]

    def get_selected_subtext(
            self: 'Tab',
    ) -> str:
        """Get the selected subtext.

        Returns:
            str: The selected subtext.
        """
        if len(self.__lines) == 0:
            return ''
        line = self.get_selected_line()
        if line.get_nb_subtext() == 0:
            return ''
        return line.get_subtext(self.__selected_subtab)

    def scroll_up(
            self: 'Tab',
    ) -> None:
        """Scroll up."""
        self.__content_scroll -= 1
        if self.__content_scroll < 0:
            self.__content_scroll = 0

    def scroll_down(
            self: 'Tab',
    ) -> None:
        """Scroll down."""
        self.__content_scroll += 1
        width = self.__content_box.get_width()
        height = self.__content_box.get_height()
        content_text = self.get_selected_subtext()
        _, line_count = addstr(content_text, width=width - 2, no_draw=True)
        max_scroll = line_count - height + 2
        if self.__content_scroll > max_scroll:
            self.__content_scroll = max_scroll

    def render_tab(
            self: 'Tab',
    ) -> None:
        """Render the tab."""
        width = self.__tab_box.get_width()
        height = self.__tab_box.get_height()
        x = self.__tab_box.get_x()
        y = self.__tab_box.get_y()

        # Set the tab color.
        tab_color = TAB_SELECTED_COLOR if self.__selected else DEFAULT_COLOR
        addstr(tab_color)

        # Minimized tab.
        if height == 0:
            # Render a simple line.
            text = '╶╴'
            addstr(text, x=x, y=y)
            text = self.__name
            used_width, _ = addstr(text, x=x + 2, y=y, width=width - 4, height=1)
            text = '╶' + '─' * (width - 4 - used_width) + '╴'
            addstr(text, x=x + 2 + used_width, y=y)
            return

        # Render top line.
        text = '┌╴'
        addstr(text, x=x, y=y)
        text = self.__name
        used_width, _ = addstr(text, x=x + 2, y=y, width=width - 4, height=1)
        text = '╶' + '─' * (width - 4 - used_width) + '┐'
        addstr(text, x=x + 2 + used_width, y=y)

        # Right line.
        if len(self.__lines) <= height - 2 or height < 6:
            # If there is no need for a scroll bar, or if the tab is too small, render a simple line.
            text = '│' * (height - 2)
        else:
            # Scroll bar.
            text = '▲'
            bar_portion = (height - 2) / len(self.__lines)
            bar_nb = max(1, int(bar_portion * (height - 4)))
            scroll_portion = self.__tab_scroll / len(self.__lines)
            scroll_nb = round(scroll_portion * (height - 4))
            text += '│' * scroll_nb
            text += '█' * bar_nb
            text += '│' * (height - 4 - scroll_nb - bar_nb)
            text += '▼'
        addstr(text, x=x + width - 1, y=y + 1, width=1, height=height - 2)

        # Left line.
        text = '│' * (height - 2)
        addstr(text, x=x, y=y + 1, width=1, height=height - 2)

        # Render bottom line.
        text = '└' + '─' * (width - 2) + '┘'
        addstr(text, x=x, y=y + height - 1, width=width, height=1)

        # Render lines.
        for i, line in enumerate(self.__lines[self.__tab_scroll:height - 2 + self.__tab_scroll]):
            line_color = LINE_SELECTED_COLOR if i + self.__tab_scroll == self.__selected_line and self.__selected else DEFAULT_COLOR
            text = line_color + line.get_text()
            addstr(text, x=x + 1, y=y + i + 1, width=width - 2, height=1)

        # Reset cursor color.
        addstr(DEFAULT_COLOR)

    def render_content(
            self: 'Tab',
    ) -> None:
        """Render the content."""
        width = self.__content_box.get_width()
        height = self.__content_box.get_height()
        y = self.__content_box.get_y()
        x = self.__content_box.get_x()

        # Render the top line.
        if len(self.__subtabs) == 0:
            text = '┌' + '─' * (width - 2) + '┐'
            addstr(text, x=x, y=y, width=width, height=1)
        else:
            colored_subtabs = [
                subtab if i != self.__selected_subtab else SUBTAB_SELECTED_COLOR + subtab + DEFAULT_COLOR
                for i, subtab in enumerate(self.__subtabs)
            ]
            addstr('┌╴', x=x, y=y)
            text = '╶╴'.join(colored_subtabs)
            used_width, _ = addstr(text, x=x + 2, y=y, width=width - 4, height=1)
            text = '╶' + '─' * (width - 4 - used_width) + '┐'
            addstr(text, x=x + 2 + used_width, y=y)

        # Render the content.
        content_text = self.get_selected_subtext()
        _, line_count = addstr(content_text, x=x + 1, y=y + 1, width=width - 2,
                               height=height - 2, scroll=self.__content_scroll)

        # Right line.
        if line_count <= height - 2 or height < 6:
            # If there is no need for a scroll bar, or if the tab is too small, render a simple line.
            right_line = '│' * (height - 2)
        else:
            # Scroll bar.
            right_line = '▲'
            bar_portion = (height - 2) / line_count
            bar_nb = max(1, int(bar_portion * (height - 4)))
            scroll_portion = self.__content_scroll / line_count
            scroll_nb = round(scroll_portion * (height - 4))
            right_line += '│' * scroll_nb
            right_line += '█' * bar_nb
            right_line += '│' * (height - 4 - scroll_nb - bar_nb)
            right_line += '▼'
        addstr(right_line, x=x + width - 1, y=y + 1, width=1, height=height - 2)

        # Left line.
        text = '│' * (height - 2)
        addstr(text, x=x, y=y + 1, width=1, height=height - 2)

        # Render the bottom line.
        text = '└' + '─' * (width - 2) + '┘'
        addstr(text, x=x, y=y + height - 1, width=width, height=1)

    def __reset_content_scroll(
            self: 'Tab',
    ) -> None:
        self.__content_scroll = 0

    def select(
            self: 'Tab',
    ) -> None:
        """Select the tab."""
        self.__selected = True

    def unselect(
            self: 'Tab',
    ) -> None:
        """Unselect the tab."""
        self.__selected = False

    def get_tab_height(
            self: 'Tab',
    ) -> int:
        """Get the tab height.

        Returns:
            int: The tab height.
        """
        return self.__tab_box.get_height()

    def get_min_height(
            self: 'Tab',
    ) -> int:
        """Get the minimum height.

        Returns:
            int: The minimum height.
        """
        return self.__min_height

    def get_height_weight(
            self: 'Tab',
    ) -> int:
        """Get the height weight.

        Returns:
            int: The height weight.
        """
        return self.__height_weight

    def __get_subtext_lines(
            self: 'Tab',
    ) -> list[str]:
        subtext = self.get_selected_subtext()
        subtext_lines = subtext.split('\n')
        width = self.__content_box.get_width() - 2
        for i, subtext_line in enumerate(subtext_lines):
            if len(subtext_line) > width:
                subtext_lines[i] = subtext_line[:width]
                subtext_lines.insert(i + 1, subtext_line[width:])
        return subtext_lines

    def __get_content_lines(
            self: 'Tab',
    ) -> list[str]:
        height = self.__content_box.get_height()
        width = self.__content_box.get_width()
        subtext_lines = self.__get_subtext_lines()
        subtext_lines = subtext_lines[self.__content_scroll:height-2+self.__content_scroll]
        subtext_lines += [' ' * (width - 2)] * (height - len(subtext_lines) - 2)
        return subtext_lines

    def __update_tab_scroll(
            self: 'Tab',
    ) -> None:
        height = self.__tab_box.get_height()
        if self.__selected_line < self.__tab_scroll:
            self.__tab_scroll = self.__selected_line
        elif self.__selected_line >= self.__tab_scroll + height - 2:
            self.__tab_scroll = self.__selected_line - height + 2 + 1
