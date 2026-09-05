import subprocess


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