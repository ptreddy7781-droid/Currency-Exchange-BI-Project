from pathlib import Path
import subprocess
import sys
from datetime import datetime


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_FOLDER = PROJECT_ROOT / "Scripts"
LOGS_FOLDER = PROJECT_ROOT / "logs"

LOGS_FOLDER.mkdir(parents=True, exist_ok=True)


def run_script(script_name: str) -> str:
    script_path = SCRIPTS_FOLDER / script_name

    if not script_path.exists():
        raise FileNotFoundError(
            f"Script not found: {script_path}"
        )

    print(f"\nRunning {script_name}...")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT
    )

    if result.stdout:
        print(result.stdout)

    if result.returncode != 0:
        if result.stderr:
            print(result.stderr)

        raise RuntimeError(
            f"{script_name} failed."
        )

    return result.stdout


def run_pipeline() -> None:
    start_time = datetime.now()

    print("=" * 60)
    print("Currency Exchange BI Pipeline")
    print("Started:", start_time)
    print("=" * 60)

    scripts = [
        "extract_currency_data.py",
        "clean_currency_data.py",
        "load_currency_to_postgresql.py"
    ]

    log_content = [
        "Currency Exchange BI Pipeline",
        f"Started: {start_time}",
        ""
    ]

    try:
        for script in scripts:
            output = run_script(script)

            log_content.append(
                f"--- {script} ---"
            )
            log_content.append(output)
            log_content.append("")

        end_time = datetime.now()
        duration = end_time - start_time

        success_message = (
            "\nPipeline completed successfully.\n"
            f"Finished: {end_time}\n"
            f"Duration: {duration}"
        )

        print(success_message)

        log_content.append(success_message)

    except Exception as error:
        failure_message = (
            "\nPipeline failed.\n"
            f"Error: {error}"
        )

        print(failure_message)

        log_content.append(failure_message)

        raise

    finally:
        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        log_file = (
            LOGS_FOLDER
            / f"pipeline_{timestamp}.log"
        )

        log_file.write_text(
            "\n".join(log_content),
            encoding="utf-8"
        )

        print("\nLog saved to:")
        print(log_file)


if __name__ == "__main__":
    run_pipeline()
    