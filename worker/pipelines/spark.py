import subprocess
from pathlib import Path

from backend.app.core.config import get_settings


class SparkPipelineRunner:
    def __init__(
        self,
        spark_submit: str = "spark-submit",
        project_root: str | None = None,
        jobs_root: str | None = None,
    ) -> None:
        settings = get_settings()

        self.spark_submit = spark_submit

        self.project_root = (
            Path(project_root)
            if project_root
            else Path(__file__).resolve().parents[2]
        )

        self.jobs_root = Path(
            jobs_root or settings.spark_jobs_root
        )

    def _resolve_script(self, script: str) -> Path:
        script_path = (self.project_root / self.jobs_root / script).resolve()
        jobs_root = (self.project_root / self.jobs_root).resolve()

        if jobs_root not in script_path.parents:
            raise ValueError(
                "Spark job must be located inside the configured "
                "Spark jobs directory."
            )

        if not script_path.is_file():
            raise ValueError(
                f"Spark job not found: {script}"
            )

        return script_path

    def run_transformation(
        self,
        *,
        script: str,
        input_path: str,
        output_path: str,
    ) -> None:
        script_path = self._resolve_script(script)

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