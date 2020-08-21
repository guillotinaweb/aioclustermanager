from aioclustermanager.deploy_list import DeployList
from aioclustermanager.k8s.deploy import K8SDeploy


class K8SDeployList(DeployList):

    def __init__(self, data=None, **kw):
        self._raw = data
        self._deploys = []
        for deploy in self._raw['items']:
            self._deploys.append(K8SDeploy(data=deploy))

    @property
    def total(self):
        return len(self._deploys)

    def values(self):
        return self._deploys
