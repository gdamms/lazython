from .line import Line
from .box import Box
from .renderer import Renderer
from .vars import *
from .shortcut import Shortcut


class Tab:
    """The tab class."""

    ID: int = 0

    def __init__(
            self: 'Tab',
            name: str = '',
            subtabs: list[str] = [],
            height_weight: float = 1,
            min_height: int = 1,
            renderer: 'Renderer' = None,
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

        self.__shortcuts: list[Shortcut] = []

        self.__selected = False

        self.__renderer = renderer

        self.id = Tab.ID
        Tab.ID += 1

    def add_key(
            self: 'Tab',
            key: int,
            callback: 'function',
            name: str = None,
            help: str = None,
    ) -> None:
        """Add a key shortcut.

        Args:
            key (int): The key.
            callback (function): The callback.
            name (str): The name. Defaults to None means no display in the menu.
            help (str): The help. Defaults to None means no display in the menu.
        """
        self.__shortcuts.append(Shortcut(key=key, callback=callback, name=name, help=help))

    def get_key_callbacks(
            self: 'Tab',
            key: int,
    ) -> list['function']:
        """Get the key callbacks.

        Args:
            key (int): The key.

        Returns:
            list[function]: The callbacks.
        """
        return [shortcut.callback for shortcut in self.__shortcuts if shortcut.key == key]

    def get_shortcuts(
            self: 'Tab',
    ) -> list[Shortcut]:
        """Get the shortcuts.

        Returns:
            list[Shortcut]: The shortcuts.
        """
        return self.__shortcuts

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

    def delete_line(
            self: 'Tab',
            line: 'Line'
    ) -> None:
        """Delete the line.

        Args:
            line (Line): The line.
        """
        self.__lines.remove(line)

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
        self.__update_content_scroll()

    def previous_line(
            self: 'Tab',
    ) -> None:
        """Select the previous line."""
        if len(self.__lines) == 0:
            return
        self.__selected_line -= 1
        self.__selected_line %= len(self.__lines)
        self.__update_tab_scroll()
        self.__update_content_scroll()

    def select_line(
            self: 'Tab',
            line: int,
    ) -> None:
        """Select the specified line.

        Args:
            line (int): The line.
        """
        self.__selected_line = line
        self.__selected_line %= len(self.__lines)
        self.__update_tab_scroll()
        self.__update_content_scroll()

    def next_subtab(
            self: 'Tab',
    ) -> None:
        """Select the next subtab."""
        if len(self.__subtabs) == 0:
            return
        self.__selected_subtab += 1
        self.__selected_subtab %= len(self.__subtabs)
        self.__update_content_scroll()

    def previous_subtab(
            self: 'Tab',
    ) -> None:
        """Select the previous subtab."""
        if len(self.__subtabs) == 0:
            return
        self.__selected_subtab -= 1
        self.__selected_subtab %= len(self.__subtabs)
        self.__update_content_scroll()

    def get_selected_line(
            self: 'Tab',
    ) -> 'Line':
        """Get the selected line.

        Returns:
            Line: The selected line.
        """
        if len(self.__lines) == 0:
            return Line()
        return self.__lines[self.__selected_line]

    def get_nb_lines(
            self: 'Tab',
    ) -> int:
        """Get the number of lines.

        Returns:
            int: The number of lines.
        """
        return len(self.__lines)

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
        if len(line.get_subtexts()) == 0:
            return ''
        return line.get_subtext(self.__selected_subtab)

    def get_content_scroll(
            self: 'Tab',
    ) -> int:
        """Get the content scroll.

        Returns:
            int: The content scroll.
        """
        return self.__content_scroll

    def get_content_height(
            self: 'Tab',
    ) -> int:
        """Get the content height.

        Returns:
            int: The content height.
        """
        return self.__content_box.get_height()

    def get_content_width(
            self: 'Tab',
    ) -> int:
        """Get the content width.

        Returns:
            int: The content width.
        """
        return self.__content_box.get_width()

    def scroll_up(
            self: 'Tab',
            scroll: int = 1,
    ) -> None:
        """Scroll up."""
        line_scroll = self.get_selected_line().get_scroll(self.__selected_subtab)
        if scroll < 0 or 0 <= line_scroll < scroll:
            # Scroll to beginning.
            self.get_selected_line().set_scroll(self.__selected_subtab, 0)
            self.__content_scroll = 0
            return

        if line_scroll < 0:
            # Start from the end.
            _, line_count = Renderer.get_size(self.get_selected_subtext(), width=self.__content_box.get_width() - 2)
            new_scroll = line_count - self.__content_box.get_height() + 2
        else:
            new_scroll = self.get_selected_line().get_scroll(self.__selected_subtab)

        # Scroll up.
        new_scroll -= scroll
        new_scroll = max(0, new_scroll)
        self.get_selected_line().set_scroll(self.__selected_subtab, new_scroll)
        self.__content_scroll = new_scroll

    def scroll_down(
            self: 'Tab',
            scroll: int = 1,
    ) -> None:
        """Scroll down."""
        if scroll < 0:
            # Scroll to end.
            self.get_selected_line().set_scroll(self.__selected_subtab, -1)
            self.__content_scroll = -1
            return

        line_scroll = self.get_selected_line().get_scroll(self.__selected_subtab)
        if line_scroll < 0:
            # Nothing to scroll, alreday at the end.
            return

        _, line_count = Renderer.get_size(self.get_selected_subtext(), width=self.__content_box.get_width() - 2)
        new_scroll = self.get_selected_line().get_scroll(self.__selected_subtab)
        new_scroll += scroll
        if new_scroll > line_count - self.__content_box.get_height() + 2:
            # Scroll to end.
            self.get_selected_line().set_scroll(self.__selected_subtab, -1)
            self.__content_scroll = -1
            return

        self.get_selected_line().set_scroll(self.__selected_subtab, new_scroll)
        self.__content_scroll = new_scroll

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
        self.__renderer.addstr(tab_color)

        # Minimized tab.
        if height == 0:
            # Render a simple line.
            text = '╶╴'
            self.__renderer.addstr(text, x=x, y=y)
            text = self.__name
            used_width, _ = self.__renderer.addstr(text, x=x + 2, y=y, width=width - 4, height=1)
            text = '╶' + '─' * (width - 4 - used_width) + '╴'
            self.__renderer.addstr(text, x=x + 2 + used_width, y=y)
            return

        # Render top line.
        text = '┌╴'
        self.__renderer.addstr(text, x=x, y=y)
        text = self.__name
        used_width, _ = self.__renderer.addstr(text, x=x + 2, y=y, width=width - 4, height=1)
        text = '╶' + '─' * (width - 4 - used_width) + '┐'
        self.__renderer.addstr(text, x=x + 2 + used_width, y=y)

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
        self.__renderer.addstr(text, x=x + width - 1, y=y + 1, width=1, height=height - 2)

        # Left line.
        text = '│' * (height - 2)
        self.__renderer.addstr(text, x=x, y=y + 1, width=1, height=height - 2)

        # Render bottom line.
        text = '└' + '─' * (width - 2) + '┘'
        self.__renderer.addstr(text, x=x, y=y + height - 1, width=width, height=1)

        # Render lines.
        for i, line in enumerate(self.__lines[self.__tab_scroll:height - 2 + self.__tab_scroll]):
            line_color = LINE_COLOR
            if i + self.__tab_scroll == self.__selected_line and self.__selected:
                line_color += LINE_SELECTED_COLOR
            text = line_color + line.get_text()
            used_width, _ = self.__renderer.addstr(text, x=x + 1, y=y + i + 1, width=width - 2, height=1, wrap=False)
            text = ' ' * (width - 2 - used_width)
            self.__renderer.addstr(text, x=x + 1 + used_width, y=y + i + 1, width=width - 2 - used_width, height=1)

        # Reset cursor color.
        self.__renderer.addstr(DEFAULT_COLOR)

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
            self.__renderer.addstr(text, x=x, y=y, width=width, height=1)
        else:
            colored_subtabs = [
                subtab if i != self.__selected_subtab else SUBTAB_SELECTED_COLOR + subtab + DEFAULT_COLOR
                for i, subtab in enumerate(self.__subtabs)
            ]
            self.__renderer.addstr('┌╴', x=x, y=y)
            text = '╶╴'.join(colored_subtabs)
            used_width, _ = self.__renderer.addstr(text, x=x + 2, y=y, width=width - 4, height=1)
            text = '╶' + '─' * (width - 4 - used_width) + '┐'
            self.__renderer.addstr(text, x=x + 2 + used_width, y=y)

        # Render the content.
        content_text = self.get_selected_subtext()
        _, line_count = Renderer.get_size(content_text, width=width - 2)
        scroll = self.__content_scroll
        if scroll < 0:
            scroll = line_count - height + 2
        elif scroll > line_count - height + 2:
            scroll = line_count - height + 2
            self.get_selected_line().set_scroll(self.__selected_subtab, -1)
            self.__content_scroll = scroll
        scroll = max(0, scroll)
        self.__renderer.addstr(content_text,
                               x=x + 1, y=y + 1,
                               width=width - 2, height=height - 2,
                               scroll=scroll)

        # Right line.
        if line_count <= height - 2 or height < 6:
            # If there is no need for a scroll bar, or if the tab is too small, render a simple line.
            right_line = '│' * (height - 2)
        else:
            # Scroll bar.
            right_line = '▲'
            bar_portion = (height - 2) / line_count
            bar_nb = max(1, round(bar_portion * (height - 4)))
            max_scroll = line_count - height + 2
            if scroll > max_scroll / 2:
                # The scroll bar is at the bottom.
                scroll_nb_bottom = line_count - scroll - height + 2
                scroll_nb_bottom /= line_count
                scroll_nb_bottom = (scroll_nb_bottom * (height - 4)).__ceil__()
                scroll_nb_top = height - 4 - bar_nb - scroll_nb_bottom
            else:
                # The scroll bar is at the top.
                scroll_nb_top = scroll / line_count
                scroll_nb_top = (scroll_nb_top * (height - 4)).__ceil__()
                scroll_nb_bottom = height - 4 - bar_nb - scroll_nb_top
            right_line += '│' * scroll_nb_top
            right_line += '█' * bar_nb
            right_line += '│' * scroll_nb_bottom
            right_line += '▼'
        self.__renderer.addstr(right_line, x=x + width - 1, y=y + 1, width=1, height=height - 2)

        # Left line.
        text = '│' * (height - 2)
        self.__renderer.addstr(text, x=x, y=y + 1, width=1, height=height - 2)

        # Render the bottom line.
        text = '└' + '─' * (width - 2) + '┘'
        self.__renderer.addstr(text, x=x, y=y + height - 1, width=width, height=1)

    def __update_content_scroll(
            self: 'Tab',
    ) -> None:
        self.__content_scroll = self.get_selected_line().get_scroll(self.__selected_subtab)

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
