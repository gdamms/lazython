import os
import threading
import time

from .box import Box
from .tab import Tab
from .renderer import Renderer
from .listener import Listener
from .shortcut import Shortcut


class Lazython:
    """The lazython class.

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
            refresh_delay: float = 0.1,
    ) -> None:
        """Initialize the lazython.

        Args:
            self (Lazython): _description_
            tabs_width (float, optional): The width of the tabs as a percentage of the terminal width. Defaults to 0.4.
            tabs_min_width (int, optional): The minimum width of the tabs. Defaults to 10.
            content_min_width (int, optional): The minimum width of the content. Defaults to 10.
            refresh_delay (float, optional): The refresh delay. Defaults to 0.1.
        """
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

        self.__refresh_delay = refresh_delay

        self.__shortcuts: list[Shortcut] = []

        self.__renderer = Renderer()
        self.__listener = Listener()

        self.__display_menu = False
        self.__menu_selected = 0

        self.__listener.add_key_callback(self.key_callback)
        self.__listener.add_click_callback(self.click_callback)

    def main(
            self: 'Lazython',
    ) -> None:
        """The main function.

        This function will start the lazython and will block until the lazython is stopped.
        """
        last_time = time.time()
        while self.__running:
            self.render()

            # Wait for the next frame.
            current_time = time.time()
            delay = self.__refresh_delay - (current_time - last_time)
            if delay > 0:
                time.sleep(delay)
            last_time = current_time

    def start(
            self: 'Lazython',
    ) -> None:
        """Start the lazython.

        This method will start the lazython and will block until the lazython is stopped.
        """
        if self.__running:
            raise Exception('The lazython is already running.')

        self.__running = True
        self.__renderer.start()
        threading.Thread(target=self.main).start()
        self.__listener.listen()

    def stop(
            self: 'Lazython',
    ) -> None:
        """Stop the lazython."""
        if not self.__running:
            raise Exception('The lazython is not running.')
        self.__listener.stop()
        self.__renderer.stop()
        self.__running = False

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
        new_tab = Tab(name=name, subtabs=subtabs, height_weight=height_weight,
                      min_height=min_height, renderer=self.__renderer)
        self.__tabs.append(new_tab)
        return new_tab

    def key_callback(
            self: 'Lazython',
            key: int,
    ) -> None:
        """The key callback.

        Args:
            key (int): The key code.
        """
        # Quit when `ctrl` + `c` is pressed.
        if key == 0:
            self.stop()

        # Close when `esc` or `q` is pressed.
        elif key == 27 or key == 113:
            if self.__display_menu:
                self.menu_quit()
            else:
                self.stop()

        # Focus next tab when `tab` is pressed.
        elif key == 9:
            self.next_tab()

        # Focus previous tab when `shift` + `tab` is pressed.
        elif key == 5921563:
            self.previous_tab()

        # Focus next line when `down` is pressed.
        elif key == 4348699:
            if self.__display_menu:
                self.menu_next()
            else:
                self.next_line()

        # Focus previous line when `up` is pressed.
        elif key == 4283163:
            if self.__display_menu:
                self.menu_previous()
            else:
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

        # Toggle menu when `x` is pressed.
        elif key == 120:
            self.menu_toggle()

        # Execute menu item when `enter` is pressed.
        elif key == 10:
            if self.__display_menu:
                self.menu_execute()
                self.menu_quit()

        # Execute the callbacks.
        callbacks = [shortcut.callback for shortcut in self.__shortcuts if shortcut.key == key]
        for callback in callbacks:
            callback()
        if len(callbacks) > 0:
            self.menu_quit()

        # Execute tab callbacks.
        if len(self.__tabs) > 0:
            callbacks = self.__tabs[self.__selected_tab].get_key_callbacks(key)
            for callback in callbacks:
                callback()
            if len(callbacks) > 0:
                self.menu_quit()

    def menu_toggle(
            self: 'Lazython',
    ) -> None:
        """Toggle the menu."""
        if self.__display_menu:
            self.menu_quit()
        else:
            self.menu_open()

    def menu_next(
            self: 'Lazython',
    ) -> None:
        """Select the next menu item."""
        self.__menu_selected += 1
        shorcuts = [shortcut for shortcut in self.__shortcuts if shortcut.displayable()] + \
            [shortcut for shortcut in self.__tabs[self.__selected_tab].get_shortcuts() if shortcut.displayable()]
        if self.__menu_selected >= len(shorcuts):
            self.__menu_selected = len(shorcuts) - 1

    def menu_previous(
            self: 'Lazython',
    ) -> None:
        """Select the previous menu item."""
        self.__menu_selected -= 1
        if self.__menu_selected < 0:
            self.__menu_selected = 0

    def menu_open(
            self: 'Lazython',
    ) -> None:
        """Open the menu."""
        self.__display_menu = True
        self.__menu_selected = 0

    def menu_quit(
            self: 'Lazython',
    ) -> None:
        """Quit the menu."""
        self.__display_menu = False
        self.__menu_selected = 0

    def menu_execute(
            self: 'Lazython',
    ) -> None:
        """Execute the selected menu item."""
        if self.__menu_selected < len(self.__shortcuts):
            self.__shortcuts[self.__menu_selected].callback()
        else:
            self.__tabs[self.__selected_tab].get_shortcuts()[self.__menu_selected - len(self.__shortcuts)].callback()

    def __render_menu(
            self: 'Lazython',
    ) -> None:
        """Render the menu."""
        # Get the menu size.
        shortcuts = [shortcut for shortcut in self.__shortcuts if shortcut.displayable()] + \
            [shortcut for shortcut in self.__tabs[self.__selected_tab].get_shortcuts() if shortcut.displayable()]
        menu_width = max([len(shortcut.name) for shortcut in shortcuts])
        menu_width += max([len(shortcut.help) for shortcut in shortcuts])
        menu_width += len(sep := ' : ')
        menu_width += 2
        menu_height = len(shortcuts) + 2
        if menu_width > self.__width:
            menu_width = self.__width
        if menu_height > self.__height - 1:
            menu_height = self.__height - 1

        # Get the menu position.
        menu_x = self.__width // 2 - menu_width // 2
        menu_y = self.__height // 2 - menu_height // 2

        # Render top border.
        title = 'Menu'
        text = '┌╴' + title + '╶' + '─' * (menu_width - 4 - len(title)) + '┐'
        self.__renderer.addstr(text, x=menu_x, y=menu_y)

        # Render bottom border.
        text = '└' + '─' * (menu_width - 2) + '┘'
        self.__renderer.addstr(text, x=menu_x, y=menu_y + menu_height - 1)

        # Render left border.
        text = '│' * (menu_height - 2)
        self.__renderer.addstr(text, x=menu_x, y=menu_y + 1, width=1)

        # Render right border.
        text = '│' * (menu_height - 2)
        self.__renderer.addstr(text, x=menu_x + menu_width - 1, y=menu_y + 1, width=1)

        # Render shortcuts.
        shortcut_width = max([len(shortcut.name) for shortcut in shortcuts])
        for i, shortcut in enumerate(shortcuts):
            text = shortcut.name + ' ' * (shortcut_width - len(shortcut.name)) + sep + shortcut.help
            color = '\x1b[7m' if i == self.__menu_selected else ''
            end_color = '\x1b[0m' if i == self.__menu_selected else ''
            self.__renderer.addstr(color + text + end_color, x=menu_x + 1,
                                   y=menu_y + 1 + i, width=menu_width - 2, height=1)

    def click_callback(
            self: 'Lazython',
            key: int,
            x: int,
            y: int,
    ) -> None:
        """The click callback.

        Args:
            key (int): The key code.
            x (int): The x.
            y (int): The y.
        """
        if len(self.__tabs) == 0:
            return

        if key == 0:
            # Left click.
            if x < self.__tabs_box.get_width():
                # Tab click.
                current_y = 0
                for i, tab in enumerate(self.__tabs):
                    if current_y <= y < current_y + tab.get_tab_height():
                        # Select the tab.
                        self.__tabs[self.__selected_tab].unselect()
                        self.__selected_tab = i
                        self.__tabs[self.__selected_tab].select()

                        # Select the line.
                        line = y - current_y - 1
                        if line < 0:
                            break
                        if line >= self.__tabs[self.__selected_tab].get_nb_lines():
                            break

                        self.__tabs[self.__selected_tab].select_line(line)
                        break
                    current_y += tab.get_tab_height() if tab.get_tab_height() > 0 else 1
            else:
                # Content click.
                # TODO: Select the subtab.
                pass

        elif key == 64:
            # Scroll up.
            self.scroll_up()
        elif key == 65:
            # Scroll down.
            self.scroll_down()

    def add_key(
            self: 'Lazython',
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

        self.__renderer.clear()

        if len(self.__tabs) == 0:
            self.__renderer.addstr('No tab.')
            self.__render_footer()
            self.__renderer.refresh()
            return

        if not self.is_renderable():
            self.__renderer.addstr('Terminal too small.')
            self.__render_footer()
            self.__renderer.refresh()
            return

        for tab in self.__tabs:
            tab.render_tab()

        tab = self.__tabs[self.__selected_tab]
        tab.render_content()

        if self.__display_menu:
            self.__render_menu()

        self.__render_footer()

        self.__renderer.refresh()

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
        text = 'Tab/Shift+Tab: Switch tab | ↑ ↓: Switch line | ← →: Switch subtab | x: Menu | q: Quit'
        self.__renderer.addstr(text[:self.__width], x=0, y=self.__height - 1)
