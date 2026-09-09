from unittest.mock import Mock, patch

from worker.pipelines.staging import HDFSStagingClient


def test_create_directory_success():
    client = HDFSStagingClient(
        webhdfs_url="http://localhost:9870"
    )

    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = {
        "boolean": True
    }

    with patch(
        "worker.pipelines.staging.httpx.put",
        return_value=response,
    ) as mock_put:
        client.create_directory(
            "/data/smart_transportation/staging"
        )

    mock_put.assert_called_once_with(
        "http://localhost:9870/webhdfs/v1/data/smart_transportation/staging",
        params={
            "op": "MKDIRS",
            "user.name": "spark",
        },
        timeout=30.0,
    )


def test_write_text_success():
    client = HDFSStagingClient(
        webhdfs_url="http://localhost:9870",
        hdfs_user="spark",
    )

    mkdir_response = Mock()
    mkdir_response.raise_for_status.return_value = None
    mkdir_response.json.return_value = {
        "boolean": True
    }

    redirect_response = Mock()
    redirect_response.status_code = 307
    redirect_response.headers = {
        "Location": (
            "http://datanode:9864"
            "/webhdfs/v1/data/smart_transportation/"
            "staging/test.json"
            "?op=CREATE"
            "&user.name=spark"
            "&namenoderpcaddress=namenode:9000"
            "&createflag="
            "&createparent=true"
            "&overwrite=true"
        )
    }

    create_response = Mock()
    create_response.status_code = 201
    create_response.raise_for_status.return_value = None

    with patch(
        "worker.pipelines.staging.httpx.put",
        side_effect=[
            mkdir_response,
            redirect_response,
            create_response,
        ],
    ) as mock_put:
        client.write_text(
            "/data/smart_transportation/staging/test.json",
            '{"value": 1}',
        )

    assert mock_put.call_count == 3

    mock_put.assert_any_call(
        "http://localhost:9870/webhdfs/v1/data/smart_transportation/staging",
        params={
            "op": "MKDIRS",
            "user.name": "spark",
        },
        timeout=30.0,
    )

    mock_put.assert_any_call(
        "http://localhost:9870/webhdfs/v1/data/smart_transportation/staging/test.json",
        params={
            "op": "CREATE",
            "overwrite": "true",
            "user.name": "spark",
        },
        content=b'{"value": 1}',
        timeout=30.0,
        follow_redirects=False,
    )

    mock_put.assert_any_call(
        "http://localhost:9864/webhdfs/v1/data/smart_transportation/staging/test.json",
        params={
            "op": "CREATE",
            "user.name": "spark",
            "namenoderpcaddress": "namenode:9000",
            "createflag": "",
            "createparent": "true",
            "overwrite": "true",
        },
        content=b'{"value": 1}',
        timeout=30.0,
    )

def test_ensure_staging_directory_normalizes_path():
    client = HDFSStagingClient(
        webhdfs_url="http://localhost:9870"
    )

    with patch.object(
        client,
        "create_directory",
    ) as mock_create_directory:
        client.ensure_staging_directory(
            "/data/smart_transportation/staging/"
        )

    mock_create_directory.assert_called_once_with(
        "/data/smart_transportation/staging"
    )