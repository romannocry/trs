class UnicornException(Exception):
    def __init__(self, name: str, label: str):
        self.name = name
        self.label = label