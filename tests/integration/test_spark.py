import subprocess


def test_spark_runtime():
    result = subprocess.run(
        [
            "docker",
            "exec",
            "bigdata-spark",
            "/opt/spark/bin/spark-submit",
            "--version",
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    output = result.stdout + result.stderr

    assert "version" in output.lower()