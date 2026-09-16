import subprocess

from uuid import uuid4

from worker.pipelines.staging import HDFSStagingClient


def test_hdfs_connection():
    result = subprocess.run(
        [
            "docker",
            "exec",
            "bigdata-namenode",
            "hdfs",
            "dfsadmin",
            "-report",
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    assert "Live datanodes (1)" in result.stdout

def test_hdfs_staging_write():
    client = HDFSStagingClient(
        webhdfs_url="http://localhost:9870"
    )

    hdfs_path = (
        "/data/smart_transportation/staging/"
        f"integration/{uuid4()}/sample.json"
    )

    content = '{"test": "staging"}'

    client.write_text(
        hdfs_path=hdfs_path,
        content=content,
    )