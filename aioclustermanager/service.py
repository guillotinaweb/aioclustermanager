class Service:
    """Generic job class."""

    def __init__(self, namespace=None, name=None, ports=None, selector=None, type=None, data=None, **kw):
        if data is not None:
            self._raw = data
        else:
            self._raw = self.create(
                namespace,
                name=name,
                ports=ports,
                selector=selector,
                type=type,
                **kw)

    @property
    def id(self):
        raise NotImplementedError()

    def get_payload(self):
        raise NotImplementedError()

    def payload(self):
        return self._raw
