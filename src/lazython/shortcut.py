class Shortcut:
    def __init__(self: 'Shortcut', key: int, name: str, help: str, callback: 'function'):
        self.key = key
        self.name = name
        self.help = help
        self.callback = callback
