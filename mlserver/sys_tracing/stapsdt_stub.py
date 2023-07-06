class Provider(object):
    def __init__(self, name):
        self._name = name
        self._provider = None
        self._probes = []

    def __str__(self):
        return self.name

    def add_probe(self, name, *args):
        probe = Probe(self, name, *args)
        self._probes.append(probe)
        return probe

    def load(self) -> bool:
        return False

    def unload(self):
        return True


class Probe:
    def __init__(self, *args):
        self._args = args

    def fire(self, *args):
        return False

    @property
    def is_enabled(self):
        return False
