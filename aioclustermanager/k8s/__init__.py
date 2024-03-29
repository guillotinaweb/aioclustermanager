from aioclustermanager.k8s.caller import K8SCaller
from base64 import b64decode

import aiohttp
import asyncio
import logging
import os
import ssl
import tempfile

logger = logging.getLogger("aioclustermanager")

SERVICE_HOST_ENV_NAME = "KUBERNETES_SERVICE_HOST"
SERVICE_PORT_ENV_NAME = "KUBERNETES_SERVICE_PORT"
SERVICE_TOKEN_ENV_NAME = "KUBERNETES_SERVICE_TOKEN"
SERVICE_TOKEN_FILENAME = "/var/run/secrets/kubernetes.io/serviceaccount/token"
SERVICE_CERT_FILENAME = "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"


def _join_host_port(host, port):
    template = "%s:%s"
    host_requires_bracketing = ":" in host or "%" in host
    if host_requires_bracketing:
        template = "[%s]:%s"
    return template % (host, port)


class Configuration:
    file = None
    ssl_context = None
    cert_file = None
    scheme = "https"

    def __init__(self, environment, loop=None):
        self.headers = {}
        self.ssl_context = None
        self.basic_auth = None
        if loop is None:
            self.loop = asyncio.get_event_loop()
        else:
            self.loop = loop

        self.environment = environment

        # Authentication
        auth = self.environment.get("auth", "in_cluster")
        if auth == "in_cluster":
            self.load_in_cluster()
        elif auth == "certificate":
            self.load_certificate()
        elif auth == "certificate_file":
            self.load_certificate_file()
        elif auth == "basic_auth":
            self.basic_auth = aiohttp.BasicAuth(
                self.environment["user"], self.environment["credentials"]
            )
        elif auth == "token":
            self.headers = {
                "Authorization": "Bearer "
                + b64decode(self.environment["token"]).decode("utf-8")
            }

        # We create the aiohttp client session
        if self.environment.get("skip_ssl", "false").lower() == "true":
            self.ssl_context = False
        else:
            if self.ssl_context is None:
                self.ssl_context = ssl.create_default_context()

            if self.environment.get("ca") is not None:
                self.ssl_context.load_verify_locations(
                    cadata=b64decode(self.environment["ca"]).decode("utf-8")
                )
            elif self.environment.get("ca_file") is not None:
                self.ssl_context = ssl.create_default_context()
                self.ssl_context.load_verify_locations(
                    cafile=self.environment["ca_file"]
                )

        if "http_scheme" in environment:
            self.scheme = self.environment["http_scheme"]

        conn = aiohttp.TCPConnector(ssl=self.ssl_context, loop=self.loop)
        self.session = aiohttp.ClientSession(
            connector=conn, headers=self.headers, loop=self.loop
        )

    def load_in_cluster(self):
        # If the pod is running in cluster
        if SERVICE_TOKEN_ENV_NAME in os.environ:
            token = os.environ[SERVICE_TOKEN_ENV_NAME]
        else:
            with open(SERVICE_TOKEN_FILENAME) as fi:
                token = fi.read()
        self.headers = {"Authorization": "Bearer " + token}
        self.environment.update(
            {
                "ca_file": SERVICE_CERT_FILENAME,
                "endpoint": _join_host_port(
                    os.environ[SERVICE_HOST_ENV_NAME], os.environ[SERVICE_PORT_ENV_NAME]
                ),
            }
        )

    def load_certificate_file(self):
        self.ssl_context = ssl.create_default_context()
        if "key" in self.environment:
            self.ssl_context.load_cert_chain(
                certfile=self.environment["certificate"],
                keyfile=self.environment["key"],
            )
        else:
            self.ssl_context.load_cert_chain(certfile=self.environment["certificate"])

    def load_certificate(self):
        self.ssl_context = ssl.create_default_context()
        self.cert_file = tempfile.NamedTemporaryFile(delete=False)
        self.cert_file.write(b64decode(self.environment["certificate"]))
        self.cert_file.close()
        self.client_key = tempfile.NamedTemporaryFile(delete=False)
        self.client_key.write(b64decode(self.environment["key"]))
        self.client_key.close()
        self.ssl_context.load_cert_chain(
            certfile=self.cert_file.name, keyfile=self.client_key.name
        )


class K8SContextManager:
    def __init__(self, environment, loop=None):
        self.environment = environment
        if loop is None:
            self.loop = asyncio.get_event_loop()
        else:
            self.loop = loop

    async def __aenter__(self):
        return await self.open()

    async def open(self):
        self.config = Configuration(self.environment, self.loop)
        return K8SCaller(
            self.config.ssl_context,
            self.environment["endpoint"],
            self.config.session,
            scheme=self.config.scheme,
        )

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def close(self):
        if self.config.file is not None:
            os.unlink(self.config.file.name)
        await self.config.session.close()


async def create_k8s_caller(environment):
    config = Configuration(environment)
    return K8SCaller(
        config.ssl_context,
        environment["endpoint"],
        config.session,
        scheme=config.scheme,
    )
