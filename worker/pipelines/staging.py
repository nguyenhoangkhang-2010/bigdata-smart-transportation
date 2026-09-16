from pathlib import PurePosixPath
from urllib.parse import urlparse

import httpx

from backend.app.core.config import get_settings


class HDFSStagingClient:
    def __init__(
        self,
        webhdfs_url: str | None = None,
        hdfs_user: str | None = None,
    ) -> None:
        settings = get_settings()

        self.webhdfs_url = (
            webhdfs_url or settings.hdfs_webhdfs_url
        ).rstrip("/")

        self.hdfs_user = (
            hdfs_user or settings.hdfs_user
        )

    def create_directory(self, hdfs_path: str) -> None:
        response = httpx.put(
            f"{self.webhdfs_url}/webhdfs/v1{hdfs_path}",
            params={
                "op": "MKDIRS",
                "user.name": self.hdfs_user,
            },
            timeout=30.0,
        )

        response.raise_for_status()

        result = response.json()

        if not result.get("boolean", False):
            raise RuntimeError(
                f"Failed to create HDFS directory: {hdfs_path}"
            )

    def write_text(
        self,
        hdfs_path: str,
        content: str,
    ) -> None:
        normalized_path = str(
            PurePosixPath(hdfs_path)
        )

        parent_path = str(
            PurePosixPath(normalized_path).parent
        )

        self.ensure_staging_directory(parent_path)

        response = httpx.put(
            f"{self.webhdfs_url}/webhdfs/v1{normalized_path}",
            params={
                "op": "CREATE",
                "overwrite": "true",
                "user.name": self.hdfs_user,
            },
            content=content.encode("utf-8"),
            timeout=30.0,
            follow_redirects=False,
        )

        if response.status_code in (301, 302, 303, 307, 308):
            location = response.headers.get("Location")

            if not location:
                raise RuntimeError(
                    "WebHDFS CREATE response did not provide "
                    "a redirect location."
                )

            redirect = urlparse(location)

            redirect_host = redirect.hostname
            redirect_port = redirect.port

            configured = urlparse(self.webhdfs_url)

            if redirect_host not in {"localhost", "127.0.0.1"}:
                redirect_host = configured.hostname

            if redirect_port is None:
                redirect_port = configured.port

            redirected_url = (
                f"{configured.scheme}://"
                f"{redirect_host}:{redirect_port}"
                f"{redirect.path}"
            )

            response = httpx.put(
                redirected_url,
                params=dict(
                    item.split("=", 1)
                    for item in redirect.query.split("&")
                    if "=" in item
                ),
                content=content.encode("utf-8"),
                timeout=30.0,
            )

        response.raise_for_status()

    def ensure_staging_directory(
        self,
        staging_path: str,
    ) -> None:
        normalized_path = str(
            PurePosixPath(staging_path)
        )

        self.create_directory(normalized_path)