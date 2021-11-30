from aioclustermanager.statefulset_list import StatefulSetList
from aioclustermanager.k8s.statefulset import K8SStatefulSet


class K8SStatefulSetList(StatefulSetList):

    def __init__(self, data=None, **kw):
        self._raw = data
        self._statefulsets = []
        for statefulset in self._raw['items']:
            self._statefulsets.append(K8SStatefulSet(data=statefulset))

    @property
    def total(self):
        return len(self._statefulsets)

    def values(self):
        return self._statefulsets
