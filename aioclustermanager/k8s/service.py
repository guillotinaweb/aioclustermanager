from aioclustermanager.service import Service
from copy import deepcopy

import json

K8S_SERVICE = {
    "kind": "Service",
    "metadata": {"name": "", "namespace": "", "labels": {}},
    "spec": {"ports": [], "selector": {}, "type": "ClusterIP"},
}


class K8SService(Service):
    @property
    def id(self):
        return self._raw["metadata"]["name"]

    def create(self, namespace, name, ports, selector, type, **kw):
        service_info = deepcopy(K8S_SERVICE)
        service_info["metadata"]["name"] = name
        service_info["metadata"]["namespace"] = namespace
        if kw.get("service_labels") is not None:
            service_info["metadata"]["service_labels"] = kw.get("service_labels")

        service_info["spec"]["ports"] = ports
        service_info["spec"]["selector"] = selector
        service_info["spec"]["type"] = type

        return service_info
