from aioclustermanager.deploy import Deploy
from copy import deepcopy

import json

K8S_DEPLOY = {
    "kind": "Deployment",
    "metadata": {"name": "", "namespace": ""},
    "spec": {
        "replicas": 1,
        "revisionHistoryLimit": 2,
        "selector": {"matchLabels": {}},
        "template": {
            "metadata": {"labels": {}},
            "spec": {
                "terminationGracePeriodSeconds": 10,
                "dnsPolicy": "ClusterFirst",
                "containers": [
                    {
                        "name": "container",
                        "image": "",
                        "resources": {"limits": {}},
                        "imagePullPolicy": "IfNotPresent",
                        "ports": []
                    }
                ],
            },
        },
    },
}


class K8SDeploy(Deploy):
    @property
    def active(self):
        status = self._raw["status"]
        return False if "active" not in status else status["active"]

    @property
    def selector(self):
        return self._raw["spec"]["selector"]["matchLabels"]

    @property
    def id(self):
        return self._raw["metadata"]["name"]

    @property
    def command(self):
        return self._raw["spec"]["template"]["spec"]["containers"][0]["command"]  # noqa

    @property
    def image(self):
        return self._raw["spec"]["template"]["spec"]["containers"][0]["image"]

    def create(self, namespace, name, image, **kw):
        deploy_info = deepcopy(K8S_DEPLOY)
        deploy_info["metadata"]["name"] = name
        deploy_info["metadata"]["namespace"] = namespace
        deploy_info["spec"]["template"]["metadata"]["name"] = name
        deploy_info["spec"]["template"]["spec"]["containers"][0]["image"] = image

        if "container" in kw and kw["container"] is not None:
            deploy_info["spec"]["template"]["spec"]["containers"][0]["name"] = kw["container"]

        if "labels" in kw and kw["labels"] is not None:
            deploy_info["metadata"]["labels"] = kw["labels"]
            deploy_info["spec"]["selector"]["matchLabels"] = kw["labels"]
            deploy_info["spec"]["selector"]["matchLabels"] = kw["labels"]
            deploy_info["spec"]["template"]["metadata"]["labels"] = kw["labels"]

        if "pullSecrets" in kw and kw["pullSecrets"] is not None:
            deploy_info["spec"]["template"]["spec"]["imagePullSecrets"] = []
            deploy_info["spec"]["template"]["spec"]["imagePullSecrets"].append(
                {"name": kw["pullSecrets"]}
            )

        if "imagePullPolicy" in kw and kw["imagePullPolicy"] is not None:
            deploy_info["spec"]["template"]["spec"]["containers"][0][
                "imagePullPolicy"
            ] = kw[
                "imagePullPolicy"
            ]  # noqa

        if "entrypoint" in kw and kw["entrypoint"] is not None:
            deploy_info["spec"]["template"]["spec"]["containers"][0]["entrypoint"] = kw[
                "entrypoint"
            ]  # noqa

        if "ports" in kw and kw["ports"] is not None:
            deploy_info["spec"]["template"]["spec"]["containers"][0]["ports"] = kw[
                "ports"
            ]  # noqa

        if "command" in kw and kw["command"] is not None:
            deploy_info["spec"]["template"]["spec"]["containers"][0]["command"] = kw[
                "command"
            ]  # noqa

        if "args" in kw and kw["args"] is not None:
            deploy_info["spec"]["template"]["spec"]["containers"][0]["args"] = kw[
                "args"
            ]  # noqa

        if "mem_limit" in kw and kw["mem_limit"] is not None:
            deploy_info["spec"]["template"]["spec"]["containers"][0]["resources"][
                "limits"
            ]["memory"] = kw[
                "mem_limit"
            ]  # noqa

        if "cpu_limit" in kw and kw["cpu_limit"] is not None:
            deploy_info["spec"]["template"]["spec"]["containers"][0]["resources"][
                "limits"
            ]["cpu"] = kw[
                "cpu_limit"
            ]  # noqa

        if "volumes" in kw and kw["volumes"] is not None:
            deploy_info["spec"]["template"]["spec"]["volumes"] = kw["volumes"]

        if "volumeMounts" in kw and kw["volumeMounts"] is not None:
            deploy_info["spec"]["template"]["spec"]["containers"][0][
                "volumeMounts"
            ] = kw[
                "volumeMounts"
            ]  # noqa

        if "replicas" in kw and kw["replicas"] is not None:
            deploy_info["spec"]["replicas"] = kw["replicas"]

        if "envFrom" in kw and kw["envFrom"] is not None:
            deploy_info["spec"]["template"]["spec"]["containers"][0]["envFrom"] = kw[
                "envFrom"
            ]  # noqa

        if "envvars" in kw and kw["envvars"] is not None:
            envlist = []
            for key, value in kw["envvars"].items():
                envlist.append({"name": key, "value": value})
            deploy_info["spec"]["template"]["spec"]["containers"][0][
                "env"
            ] = envlist  # noqa

        if "annotations" in kw and kw["annotations"] is not None:
            deploy_info["spec"]["template"]["metadata"]["annotations"] = kw["annotations"]

        if "affinity" in kw and kw["affinity"] is not None:
            deploy_info["spec"]["template"]["spec"]["affinity"] = kw["affinity"]

        if "nodeSelector" in kw and kw["nodeSelector"] is not None:
            deploy_info["spec"]["template"]["spec"]["nodeSelector"] = kw["nodeSelector"]

        if "tolerations" in kw and kw["tolerations"] is not None:
            deploy_info["spec"]["template"]["spec"]["tolerations"] = kw["tolerations"]

        if "securityContext" in kw and kw["securityContext"] is not None:
            deploy_info["spec"]["template"]["spec"]["containers"][0]["securityContext"] = kw[
                "securityContext"
            ]
        
        if "readinessProbe" in kw and kw["readinessProbe"] is not None:
            deploy_info["spec"]["template"]["spec"]["containers"][0]["readinessProbe"] = kw[
                "readinessProbe"
            ]
        
        if "livenessProbe" in kw and kw["livenessProbe"] is not None:
            deploy_info["spec"]["template"]["spec"]["containers"][0]["livenessProbe"] = kw[
                "livenessProbe"
            ]

        return deploy_info

    def get_payload(self):
        container = self._raw["spec"]["template"]["spec"]["containers"][0]
        for env in container.get("env") or []:
            if env["name"] == "PAYLOAD":
                data = env["value"]
                return json.loads(data)
        return None
