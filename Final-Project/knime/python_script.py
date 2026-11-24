







from pathlib import Path
import sys
import knime.scripting.io as knio

project = Path(str(knio.flow_variables["loopguard_project"])).expanduser().resolve()
if not (project / "loopguard/engine.py").is_file():
    raise ValueError("loopguard_project must point to the extracted LoopGuard Python project.")
sys.path.insert(0, str(project))

from loopguard.tables import audit_tables, model_from_tables, model_fingerprint

model = model_from_tables(knio.input_tables[0].to_pandas(),
                          knio.input_tables[1].to_pandas(),
                          name=str(knio.flow_variables.get("loopguard_name", "Friendship Fair")),
                          scenario=str(knio.flow_variables.get("loopguard_scenario", "friendship-fair")))
tables = audit_tables(model)
fingerprint = model_fingerprint(model)
knio.output_tables[0] = knio.Table.from_pandas(tables["facts"].assign(model_fingerprint=fingerprint))
knio.output_tables[1] = knio.Table.from_pandas(tables["findings"])
knio.output_tables[2] = knio.Table.from_pandas(tables["trace"])
