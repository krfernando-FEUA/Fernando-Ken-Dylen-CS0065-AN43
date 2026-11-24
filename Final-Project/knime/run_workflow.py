




from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import zipfile

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd
from loopguard.engine import validate
from loopguard.tables import audit_tables, model_fingerprint
from knime.build_workflow import build_workflow


def find_knime(executable_path: str | Path | None = None) -> Path | None:

    if executable_path:
        path = Path(executable_path).expanduser()
        if not path.is_file():
            raise ValueError("The configured KNIME executable does not exist.")
        return path.resolve()
    configured = os.environ.get("LOOPGUARD_KNIME")
    if configured:
        return find_knime(configured)
    for command in ("knimec", "knime"):
        found = shutil.which(command)
        if found:
            return Path(found)
    for base in (Path(os.environ.get("LOCALAPPDATA", "")) / "Programs/KNIME",
                 Path.home() / "AppData/Local/Programs/KNIME",
                 Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "KNIME"):
        for filename in ("knimec.exe", "knime.exe"):
            path = base / filename
            if path.is_file():
                return path
    return None


def knime_status(executable_path: str | Path | None = None) -> dict:

    executable = find_knime(executable_path)
    if executable is None:
        return {"installed": False, "batch_available": False, "path": None,
                "reason": "KNIME Analytics Platform was not found."}
    plugins = executable.parent / "plugins"
    products = list(plugins.glob("org.knime.product_*/knime-product.jar")) if plugins.is_dir() else []


    for product in products:
        with zipfile.ZipFile(product) as archive:
            name = "org/knime/product/headless/KNIMEBatchApplication.class"
            content = archive.read(name) if name in archive.namelist() else b""
        if b"KNIME Batch Executor is not installed" in content:
            candidates = [path for path in plugins.iterdir() if "knime" in path.name.lower()
                          and "batch" in path.name.lower()]
            if not candidates:
                return {"installed": True, "batch_available": False, "path": str(executable),
                        "reason": "This KNIME installation requires the separate KNIME Batch Executor extension for automatic runs. Import the .knwf and execute it in KNIME, or install that extension before using the automatic comparison."}
    return {"installed": True, "batch_available": None, "path": str(executable),
            "reason": "KNIME found. Batch capability will be confirmed by execution."}


def compare_decisions(model: dict, decisions: pd.DataFrame) -> pd.DataFrame:

    required = {"cycle_id", "knime_classification", "knime_severity", "model_fingerprint"}
    if not required.issubset(decisions.columns):
        raise ValueError("KNIME output needs cycle_id, knime_classification, knime_severity and model_fingerprint columns.")
    if decisions.columns.duplicated().any() or decisions["cycle_id"].duplicated().any():
        raise ValueError("KNIME output contains duplicate columns or cycle IDs.")
    if decisions[list(required)].isna().any().any():
        raise ValueError("KNIME output contains missing decision or provenance fields.")
    if set(decisions["model_fingerprint"]) != {model_fingerprint(model)}:
        raise ValueError("This KNIME result belongs to a different economy revision. Export and run the current model.")
    expected = audit_tables(model)["cycles"][["cycle_id", "classification", "severity"]].copy()
    if set(decisions["cycle_id"]) != set(expected["cycle_id"]):
        raise ValueError("KNIME returned a different set of cycle IDs; comparison was rejected.")
    comparison = expected.merge(decisions[["cycle_id", "knime_classification", "knime_severity"]],
                                on="cycle_id", validate="one_to_one")
    comparison["matches"] = ((comparison["classification"] == comparison["knime_classification"]) &
                             (comparison["severity"] == comparison["knime_severity"]))
    return comparison


def _execute(command: list[str], timeout: int) -> tuple[int, str]:
    options = {"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {"start_new_session": True}
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **options)
    try:
        output, _ = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired as exc:

        if os.name == "nt":
            subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                           capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW, timeout=10)
        else:
            os.killpg(process.pid, signal.SIGKILL)
        try:
            process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        raise RuntimeError(f"KNIME did not finish within {timeout} seconds; this run produced no accepted result.") from exc
    return process.returncode, output.decode("utf-8", errors="replace")


def run_workflow(model: dict, executable_path: str | Path | None = None, *,
                 timeout: int = 180) -> dict:






    validation = validate(model)
    if not validation["valid"]:
        raise ValueError("Invalid economy: " + "; ".join(validation["errors"]))
    fingerprint = model_fingerprint(model)
    tables = audit_tables(model)
    expected = tables["cycles"][["cycle_id", "classification", "severity"]].copy()
    if expected.empty:
        return {"status": "empty", "executed": False, "matched": None,
                "fingerprint": fingerprint, "seconds": 0.0,
                "decisions": pd.DataFrame({key: pd.Series(dtype="string") for key in
                                           ("cycle_id", "knime_classification", "knime_severity")}),
                "comparison": expected, "log": "No currency return paths were found; KNIME was not invoked."}
    executable = find_knime(executable_path)
    if executable is None:
        raise FileNotFoundError("KNIME was not found. Install KNIME Analytics Platform or set LOOPGUARD_KNIME to its executable.")
    status = knime_status(executable)
    if status["batch_available"] is False:
        raise RuntimeError(status["reason"])
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="loopguard-knime-", ignore_cleanup_errors=True) as temporary:
        root = Path(temporary)
        source = root / "cycle_facts.csv"
        tables["facts"].assign(model_fingerprint=fingerprint).to_csv(source, index=False)
        workflow = build_workflow(root / "LoopGuard Friendship Fair", source)
        command = [str(executable), "-nosplash", "-application", "org.knime.product.KNIME_BATCH_APPLICATION",
                   "-data", str(root / "workspace"), "-workflowDir=" + str(workflow),
                   "-reset", "-nosave", "-consoleLog"]
        returncode, log = _execute(command, timeout)
        output = workflow / "data/decisions.csv"
        if returncode != 0 or not output.is_file():
            raise RuntimeError(f"KNIME execution failed (exit {returncode}).\n" + log[-12000:])
        decisions = pd.read_csv(output, dtype={"cycle_id": "string", "knime_classification": "string", "knime_severity": "string"})
        comparison = compare_decisions(model, decisions)
        matched = bool(comparison["matches"].fillna(False).all())
        return {"status": "matched" if matched else "mismatch", "executed": True,
                "matched": matched, "fingerprint": fingerprint,
                "seconds": round(time.monotonic() - started, 2),
                "decisions": decisions, "comparison": comparison, "log": log[-20000:]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run native KNIME decision rules against the current Python economy.\n\nEvery invocation creates a separate workspace and workflow; no stale outputs or\nuser KNIME workspaces are reused. Inputs and outputs are tied to a SHA-256 hash.\n')
    parser.add_argument("model", type=Path, help="A loopguard-v1 economy JSON file")
    parser.add_argument("--knime", type=Path, help="KNIME executable (auto-detected by default)")
    parser.add_argument("--output", type=Path, default=Path("knime/results"))
    args = parser.parse_args()
    result = run_workflow(json.loads(args.model.read_text(encoding="utf-8")), args.knime)
    args.output.mkdir(parents=True, exist_ok=True)
    for key in ("decisions", "comparison"):
        result[key].to_csv(args.output / (key + ".csv"), index=False)
    (args.output / "run.json").write_text(json.dumps({key: result[key] for key in
        ("status", "executed", "matched", "fingerprint", "seconds")}, indent=2), encoding="utf-8")
    (args.output / "knime.log").write_text(result["log"], encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("status", "matched", "fingerprint", "seconds")}, indent=2))
