from pathlib import Path

import os
import yaml


def get_inner_config(list_info, key):
    for element in list_info:
        if element["name"] == key:
            return element


def get_k8s_config():
    home = str(Path.home())
    # Designed to run on docker desktop k8s support
    # XXX DOES NOT CURRENTLY WORK WITH containers running in k8s already
    if os.environ.get("TEST_INSIDE_K8S", False):
        config_k8s = {"auth": "in_cluster"}
        return config_k8s

    with open(home + "/.kube/config", "r") as f:
        configuration = yaml.load(f)

    TRAVIS = os.environ.get("TRAVIS", "false")
    config_k8s = {}
    # if TRAVIS == "true":
    #     # defined on testing.csv
    #     config_k8s["user"] = "testinguser"
    #     config_k8s["credentials"] = "12345678"
    #     config_k8s["auth"] = "basic_auth"
    #     cluster_info = get_inner_config(configuration["clusters"], "minikube")
    #     server_url = cluster_info["cluster"]["server"]
    #     if "://" in server_url:
    #         schema, server_url = server_url.split("://")

    #     config_k8s["endpoint"] = server_url
    #     config_k8s["http_scheme"] = schema
    #     config_k8s["ca_file"] = cluster_info["cluster"]["certificate-authority"]
    # else:
    local_cluster = None
    for context in configuration["contexts"]:
        if context["name"] == "docker-desktop":
            local_cluster = "docker-desktop"
            break
        elif context["name"] == "minikube":
            local_cluster = "minikube"
            break

    if local_cluster is None:
        raise Exception("Invalid cluster configuration")

    user_info = get_inner_config(configuration["users"], local_cluster)
    cluster_info = get_inner_config(configuration["clusters"], local_cluster)

    if TRAVIS == "true":
        config_k8s["token"] = os.environ["K8S_TOKEN"]
        config_k8s["auth"] = "token"
    elif local_cluster == "minikube":
        config_k8s["certificate"] = user_info["user"]["client-certificate"]
        config_k8s["key"] = user_info["user"]["client-key"]
        config_k8s["auth"] = "certificate_file"
    elif local_cluster == "docker-desktop":
        config_k8s["certificate"] = user_info["user"]["client-certificate-data"]
        config_k8s["key"] = user_info["user"]["client-key-data"]
        config_k8s["auth"] = "certificate"

    server_url = cluster_info["cluster"]["server"]
    schema = "http"
    if "://" in server_url:
        schema, server_url = server_url.split("://")
    config_k8s["endpoint"] = server_url
    config_k8s["http_scheme"] = schema
    config_k8s["skip_ssl"] = (
        "true" if cluster_info["cluster"].get("insecure-skip-tls-verify", False) else "false"
    )
    if config_k8s["skip_ssl"] == "false":
        ca_info = cluster_info["cluster"].get("certificate-authority-data")
        if ca_info is None:
            ca_info = cluster_info["cluster"].get("certificate-authority")
            config_k8s["ca_file"] = ca_info
        else:
            config_k8s["ca"] = ca_info

    return config_k8s
