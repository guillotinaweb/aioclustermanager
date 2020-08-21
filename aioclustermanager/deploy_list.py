class DeployList:
    """Generic deploy class."""

    def __init__(self, data=None, **kw):
        self._raw = data

    @property
    def values(self):
        raise NotImplementedError()

    def __len__(self):
        return len(self.values())

    def __iter__(self):
        for deploy in self.values():
            yield deploy
