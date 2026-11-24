
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from loopguard.tables import audit_tables, model_to_tables
from knime.build_workflow import archive_workflow, build_workflow
from knime.run_workflow import model_fingerprint


def export_bundle(model: dict, destination: str | Path) -> Path:

    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    items, transactions = model_to_tables(model)
    items.to_csv(destination / "items.csv", index=False)
    transactions.to_csv(destination / "transactions.csv", index=False)
    tables = audit_tables(model)
    for name, frame in tables.items():
        if name == "facts":
            frame = frame.assign(model_fingerprint=model_fingerprint(model))
        frame.to_csv(destination / ("cycle_facts.csv" if name == "facts" else name + ".csv"), index=False)
    (destination / "model.json").write_text(json.dumps(model, indent=2, ensure_ascii=False), encoding="utf-8")
    metadata = {"schema": "loopguard-knime-export-v1", "fingerprint": model_fingerprint(model),
                "model": model["name"], "scenario": model["scenario"],
                "cycles": len(tables["cycles"]), "nativeExecutionVerified": False}
    (destination / "manifest.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    workflow = build_workflow(destination / "LoopGuard Friendship Fair", destination / "cycle_facts.csv")

    for name in ("model.json", "manifest.json"):
        (workflow / "data" / name).write_bytes((destination / name).read_bytes())
    archive = destination / "LoopGuard_Friendship_Fair.knwf"
    archive_workflow(workflow, archive)
    return archive


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export the current model's typed reports and a portable native KNIME workflow.")
    parser.add_argument("model", type=Path)
    parser.add_argument("--output", type=Path, default=Path("knime/current-model"))
    args = parser.parse_args()
    print(export_bundle(json.loads(args.model.read_text(encoding="utf-8")), args.output))
