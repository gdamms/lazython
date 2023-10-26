class Shortcut:
    def __init__(self: 'Shortcut', key: int, callback: 'function', name: str = None, help: str = None):
        self.key = key
        self.callback = callback
        self.name = name
        self.help = help

    def displayable(self: 'Shortcut') -> bool:
        return self.name is not None and self.help is not None
