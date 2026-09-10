import subprocess
from pathlib import Path


class SparkPipelineRunner:
    def __init__(
        self,
        spark_submit: str = "spark-submit",
        project_root: str | None = None,
    ) -> None:
        self.spark_submit = spark_submit

        self.project_root = (
            Path(project_root)
            if project_root
            else Path(__file__).resolve().parents[2]
        )

    def run_transformation(
        self,
        input_path: str,
        output_path: str,
    ) -> None:
        script_path = (
            self.project_root
            / "spark"
            / "jobs"
            / "transform_tlc.py"
        )

        command = [
            self.spark_submit,
            str(script_path),
            "--input",
            input_path,
            "--output",
            output_path,
        ]

        result = subprocess.run(
            command,
            cwd=self.project_root,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                "Spark transformation failed.\n"
                f"STDOUT:\n{result.stdout}\n"
                f"STDERR:\n{result.stderr}"
            )