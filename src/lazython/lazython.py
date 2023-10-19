import os

from .box import Box
from .tab import Tab
from .get_key import get_key
from .renderer import addstr, refresh, clear, start, stop


class Lazython:
    """The lazython class.

    Args:
        tabs_width (float, optional): The width of the tabs as a percentage of the terminal width. Defaults to 0.4.
        tabs_min_width (int, optional): The minimum width of the tabs. Defaults to 10.
        content_min_width (int, optional): The minimum width of the content. Defaults to 10.

    Methods:
        start(): Start the lazython.
        new_tab(): Create a new tab.
        update(): Perform all necessary updates.
        render(): Render the lazython.
        is_renderable(): Check if the lazython is renderable.
        is_minimized(): Check if the lazython is minimized.
        next_tab(): Focus the next tab.
        previous_tab(): Focus the previous tab.
        next_line(): Focus the next line.
        previous_line(): Focus the previous line.
        next_subtab(): Focus the next subtab.
        previous_subtab(): Focus the previous subtab.
        scroll_up(): Scroll up in the tab content.
        scroll_down(): Scroll down in the tab content.

    """

    def __init__(
            self: 'Lazython',
            tabs_width: float = 0.4,
            tabs_min_width: int = 10,
            content_min_width: int = 10,
    ) -> None:
        # TODO: Check if the arguments are valid.
        if tabs_min_width < 4:
            raise ValueError('Tabs min width must be at least 4.')
        if content_min_width < 4:
            raise ValueError('Content min width must be at least 4.')
        tabs_width = max(0, min(1, tabs_width))

        self.__tabs_width = tabs_width  # The width of the tabs as a percentage of the terminal width.
        self.__tabs_min_width = tabs_min_width  # The minimum width of the tabs.
        self.__content_min_width = content_min_width
        self.__min_height = 0  # The minimum height of the lazyier.
        self.__strict_min_height = 0  # The minimum height of the lazyier when it is minimized.

        self.__tabs: list[Tab] = []

        self.__selected_tab = 0

        self.__tabs_box = Box(width=0, height=0, x=0, y=0)
        self.__content_box = Box(width=0, height=0, x=0, y=0)

        self.__width = 0
        self.__height = 0

        self.__running = False

        self.__key_map = {}

    def start(
            self: 'Lazython',
    ) -> None:
        """Start the lazython.

        This method will start the lazython and will block until the lazython is stopped.
        """
        start()
        self.__running = True
        while self.__running:
            self.render()

            key = get_key(timeout=0.1)

            # Quit when `esc` or `q` or `ctrl` + `c` is pressed.
            if key == 27 or key == 113 or key == 0:
                self.stop()

            # Focus next tab when `tab` is pressed.
            elif key == 9:
                self.next_tab()

            # Focus previous tab when `shift` + `tab` is pressed.
            elif key == 5921563:
                self.previous_tab()

            # Focus next line when `down` is pressed.
            elif key == 4348699:
                self.next_line()

            # Focus previous line when `up` is pressed.
            elif key == 4283163:
                self.previous_line()

            # Focus next subtab when `right` is pressed.
            elif key == 4414235:
                self.next_subtab()

            # Focus previous subtab when `left` is pressed.
            elif key == 4479771:
                self.previous_subtab()

            # Scroll up when `page up` is pressed.
            elif key == 2117425947:
                self.scroll_up()

            # Scroll down when `page down` is pressed.
            elif key == 2117491483:
                self.scroll_down()

            # Execute the callbacks.
            callbacks = self.__key_map.get(key, [])
            for callback in callbacks:
                callback()
        stop()

    def stop(
            self: 'Lazython',
    ) -> None:
        """Stop the lazython."""
        self.__running = False
        stop()

    def new_tab(
            self: 'Lazython',
            name: str = '',
            subtabs: list[str] = [],
            height_weight: float = 1,
            min_height: int = 1,
    ) -> 'Tab':
        """Create a new tab.

        Args:
            name (str, optional): The tab name. Defaults to ''.
            subtabs (list[str], optional): The subtabs names. Defaults to [].
            height_weight (float, optional): The height weight of the tab in the tab list. Defaults to 1.
            min_height (int, optional): The minimum height of the tab. Defaults to 1.

        Returns:
            Tab: The new tab.
        """
        new_tab = Tab(name=name, subtabs=subtabs, height_weight=height_weight, min_height=min_height)
        self.__tabs.append(new_tab)
        return new_tab

    def add_key(
            self: 'Lazython',
            key: int,
            callback: callable,
    ) -> None:
        """Add a key callback.

        Args:
            key (int): The key code.
            callback (callable): The callback.
        """
        callbacks: list[callable] = self.__key_map.get(key, [])
        callbacks.append(callback)
        self.__key_map[key] = callbacks

    def update(
            self: 'Lazython',
    ) -> None:
        """Perform all necessary updates."""
        self.__update_sizes()
        if len(self.__tabs) == 0:
            return
        self.__tabs[self.__selected_tab].select()

    def render(
            self: 'Lazython',
    ) -> None:
        """Render the lazython."""
        self.update()

        clear()

        if len(self.__tabs) == 0:
            addstr('No tab.')
            self.__render_footer()
            refresh()
            return

        if not self.is_renderable():
            addstr('Terminal too small.')
            self.__render_footer()
            refresh()
            return

        for tab in self.__tabs:
            tab.render_tab()

        tab = self.__tabs[self.__selected_tab]
        tab.render_content()

        self.__render_footer()

        refresh()

    def is_renderable(
            self: 'Lazython',
    ) -> bool:
        """Check if the lazython is renderable.

        Returns:
            bool: True if the lazython is renderable, False otherwise.
        """
        # Check if renderable horizontally.
        if self.__tabs_box.get_width() < self.__tabs_min_width or self.__content_box.get_width() < self.__content_min_width:
            return False

        # Check if renderable vertically.
        if self.__tabs_box.get_height() < self.__strict_min_height:
            return False

        return True

    def is_minimized(
            self: 'Lazython',
    ) -> bool:
        """Check if the lazython is minimized.

        Returns:
            bool: True if the lazython is minimized, False otherwise.
        """
        return self.__tabs_box.get_height() < self.__min_height

    def next_tab(
            self: 'Lazython',
    ) -> None:
        """Focus the next tab."""
        if len(self.__tabs) == 0:
            return
        previous_tab = self.__tabs[self.__selected_tab]
        self.__selected_tab += 1
        self.__selected_tab %= len(self.__tabs)

        # Update the selected tab.
        current_tab = self.__tabs[self.__selected_tab]
        previous_tab.unselect()
        current_tab.select()

    def previous_tab(
            self: 'Lazython',
    ) -> None:
        """Focus the previous tab."""
        if len(self.__tabs) == 0:
            return
        previous_tab = self.__tabs[self.__selected_tab]
        self.__selected_tab -= 1
        self.__selected_tab %= len(self.__tabs)

        # Update the selected tab.
        current_tab = self.__tabs[self.__selected_tab]
        previous_tab.unselect()
        current_tab.select()

    def next_line(
            self: 'Lazython',
    ) -> None:
        """Focus the next line."""
        self.__tabs[self.__selected_tab].next_line()

    def previous_line(
            self: 'Lazython',
    ) -> None:
        """Focus the previous line."""
        self.__tabs[self.__selected_tab].previous_line()

    def next_subtab(
            self: 'Lazython',
    ) -> None:
        """Focus the next subtab."""
        self.__tabs[self.__selected_tab].next_subtab()

    def previous_subtab(
            self: 'Lazython',
    ) -> None:
        """Focus the previous subtab."""
        self.__tabs[self.__selected_tab].previous_subtab()

    def scroll_up(
            self: 'Lazython',
    ) -> None:
        """Scroll up in the tab content."""
        self.__tabs[self.__selected_tab].scroll_up()

    def scroll_down(
            self: 'Lazython',
    ) -> None:
        """Scroll down in the tab content."""
        self.__tabs[self.__selected_tab].scroll_down()

    def __update_sizes(
            self: 'Lazython',
    ) -> None:
        # Get the terminal size.
        size = os.get_terminal_size()
        self.__width = size.columns
        self.__height = size.lines

        # Update the boxes.
        self.__update_width()
        self.__update_height()
        self.__update_positions()

    def __update_width(
            self: 'Lazython',
    ) -> None:
        # Update self width.
        self.__tabs_box.set_width(int(self.__width * self.__tabs_width))
        self.__content_box.set_width(self.__width - self.__tabs_box.get_width())

        # Update the tabs width.
        for tab in self.__tabs:
            tab.set_tab_width(self.__tabs_box.get_width())
            tab.set_content_width(self.__content_box.get_width())

    def __update_height(
            self: 'Lazython',
    ) -> None:
        # Update self height.
        self.__tabs_box.set_height(self.__height - 1)
        self.__content_box.set_height(self.__height - 1)

        if len(self.__tabs) == 0:
            return

        self.__min_height = sum([tab.get_min_height() for tab in self.__tabs]) + 2 * len(self.__tabs)
        self.__strict_min_height = max([tab.get_min_height() for tab in self.__tabs]) + 2 + len(self.__tabs) - 1

        if self.is_minimized():
            # If minimized, all tabs only show their name but the selected one.
            available_height = self.__tabs_box.get_height() - len(self.__tabs) + 1
            for i, tab in enumerate(self.__tabs):
                if i == self.__selected_tab:
                    tab.set_tab_height(available_height)
                else:
                    # If not selected, minimize the tab.
                    tab.set_tab_height(0)
                tab.set_content_height(self.__content_box.get_height())

            # Add remaining height to the selected tab.
            selected_tab = self.__tabs[self.__selected_tab]
            selected_tab.set_tab_height(selected_tab.get_tab_height() + available_height -
                                        sum([tab.get_tab_height() for tab in self.__tabs]))
        else:
            # If not minimized, all tabs show their content.
            total_height_weight = sum([tab.get_height_weight() for tab in self.__tabs])
            available_height = self.__content_box.get_height()
            sorted_tabs = sorted(self.__tabs, key=lambda tab: tab.get_min_height(), reverse=True)
            for tab in sorted_tabs:
                tab.set_tab_height(int(tab.get_height_weight() / total_height_weight * available_height))
                if tab.get_tab_height() < tab.get_min_height() + 2:
                    tab.set_tab_height(tab.get_min_height() + 2)
                tab.set_content_height(self.__content_box.get_height())

            # Add remaining height to the last tab.
            last_tab = self.__tabs[-1]
            last_tab.set_tab_height(last_tab.get_tab_height() + available_height -
                                    sum([tab.get_tab_height() for tab in self.__tabs]))

    def __update_positions(
            self: 'Lazython',
    ) -> None:
        # Update self positions.
        self.__tabs_box.set_x(0)
        self.__tabs_box.set_y(0)
        self.__content_box.set_x(self.__tabs_box.get_width())
        self.__content_box.set_y(0)

        # Update tabs positions.
        current_y = 0
        for tab in self.__tabs:
            tab.set_tab_x(self.__tabs_box.get_x())
            tab.set_tab_y(current_y)
            current_y += tab.get_tab_height() if tab.get_tab_height() > 0 else 1
            tab.set_content_y(self.__content_box.get_y())
            tab.set_content_x(self.__content_box.get_x())

    def __render_footer(
            self: 'Lazython',
    ) -> None:
        text = 'Tab/Shift+Tab: Switch tab | ↑ ↓: Switch line | ← →: Switch subtab | q: Quit'
        addstr(text[:self.__width], x=0, y=self.__height - 1)
