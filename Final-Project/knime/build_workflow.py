






from __future__ import annotations
import argparse
import copy
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET
import zipfile

NS = "http://www.knime.org/2008/09/XMLConfig"
ET.register_namespace("", NS)

CLASSIFICATION_RULES = [
    '$profit$ = 0 => "break-even"',
    '$profit$ < 0 => "losing-route"',
    '$start_amount$ > 1000000000 => "oversized-batch"',
    '$unknown_limits$ = 1 OR $unknown_transfers$ = 1 => "unverified-repeatability"',
    '$unknown_intent$ = 1 OR $mixed_intent$ = 1 => "unverified-intent"',
    '$bounded$ = 0 AND $all_intended$ = 1 => "unbounded-intended-reward"',
    '$bounded$ = 0 => "repeatable-profit"',
    '$all_intended$ = 1 => "intended-reward"',
    '$transferable_account_cap$ = 1 AND $global_cap$ = 0 => "account-limit-risk"',
    'TRUE => "bounded-arbitrage"',
]
SEVERITY_RULES = [
    '$knime_classification$ = "break-even" OR $knime_classification$ = "losing-route" => "healthy"',
    '$knime_classification$ = "oversized-batch" OR $knime_classification$ = "unverified-repeatability" OR $knime_classification$ = "unverified-intent" => "review"',
    '$knime_classification$ = "repeatable-profit" => "critical"',
    '$knime_classification$ = "intended-reward" => "intended"',
    'TRUE => "high"',
]


def cfg(parent, key):
    return ET.SubElement(parent, f"{{{NS}}}config", {"key": key})


def entry(parent, key, value, kind=None):
    if kind is None:
        kind = "xboolean" if isinstance(value, bool) else "xint" if isinstance(value, int) else "xstring"
    return ET.SubElement(parent, f"{{{NS}}}entry", {
        "key": key, "type": kind,
        "value": str(value).lower() if isinstance(value, bool) else str(value),
    })


def write_xml(root, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    ET.indent(root, space="    ")
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)


def node(factory, name, model, label):
    root = ET.Element(f"{{{NS}}}config", {"key": "settings.xml"})
    entry(root, "node_file", "settings.xml")
    cfg(root, "flow_stack")
    entry(cfg(root, "internal_node_subsettings"), "memory_policy", "CacheSmallInMemory")
    root.append(model)
    annotation = cfg(root, "nodeAnnotation")
    for key, value in {"text": label, "contentType": "text/plain", "bgcolor": 16777215,
                       "x-coordinate": 0, "y-coordinate": 0, "width": 180, "height": 50,
                       "alignment": "CENTER", "borderSize": 0, "borderColor": 16777215,
                       "defFontSize": 11, "annotation-version": 20230412}.items():
        entry(annotation, key, value)
    cfg(annotation, "styles")
    for key, value in {"state": "IDLE", "factory": factory, "node-name": name,
                       "name": name, "hasContent": False, "isInactive": False}.items():
        entry(root, key, value)


    is_rule = factory == "org.knime.base.node.rules.engine.RuleEngineNodeFactory"
    bundle_version = "5.12.0.v202606171353" if is_rule else "5.12.0.v202606261225"
    for key, value in {
        "node-bundle-name": "KNIME Java Snippet Nodes" if is_rule else "KNIME Base Nodes",
        "node-bundle-symbolic-name": "org.knime.jsnippets" if is_rule else "org.knime.base",
        "node-bundle-vendor": "KNIME AG, Zurich, Switzerland",
        "node-bundle-version": bundle_version,
        "node-feature-name": "KNIME Javasnippet" if is_rule else "KNIME Base nodes",
        "node-feature-symbolic-name": "org.knime.features.javasnippet.feature.group" if is_rule else "org.knime.features.base.feature.group",
        "node-feature-vendor": "KNIME AG, Zurich, Switzerland",
        "node-feature-version": bundle_version,
    }.items():
        entry(root, key, value)
    cfg(root, "factory_settings")
    cfg(root, "ports")
    return root


def rule_model(column, rules):
    model = ET.Element(f"{{{NS}}}config", {"key": "model"})
    entry(model, "new-column-name", column)
    entry(model, "replace-column-name", "")
    entry(model, "append-column", True)
    entry(model, "disallowLongOutputForCompatibility", True)
    rules_cfg = cfg(model, "rules")
    entry(rules_cfg, "array-size", len(rules))
    for index, rule in enumerate(rules):
        entry(rules_cfg, str(index), rule)
    return model


def writer_model():
    model = ET.Element(f"{{{NS}}}config", {"key": "model"})
    values = {
        "filename": "knime://knime.workflow/data/decisions.csv",
        "colSeparator": ",", "quoteBegin": '"', "quoteEnd": '"',
        "quoteReplacement": '""', "quoteMode": "STRINGS", "sepReplacePattern": "",
        "ReplSepInStrings": False, "writeColHeader": True, "writeRowHeader": False,
        "missing": "", "lineEndingMode": "LF", "charSet": "UTF-8",
        "scientificExtrema": False, "commentBegin": "#", "commentEnd": "",
        "commentIndent": "", "addTime": False, "addUser": False,
        "addTablename": False, "userCommentLine": "", "skipWriteColHeaderOnAppend": True,
        "isAppendToFile": False, "fileOverwritePolicy": "Overwrite", "gzip": False,
    }
    for key, value in values.items():
        entry(model, key, value)
    entry(model, "decimalSeparator", ".", "xchar")
    return model


def build_workflow(destination: str | Path, facts_csv: str | Path) -> Path:
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "data").mkdir(exist_ok=True)
    target = destination / "data/cycle_facts.csv"
    if Path(facts_csv).resolve() != target.resolve():
        shutil.copyfile(facts_csv, target)
    reader = ET.parse(Path(__file__).parent / "templates/csv-reader-model.xml").getroot()
    specs = [
        ("CSV Reader (#1)", "CSV Reader", "org.knime.base.node.io.filehandling.csv.reader.CSVTableReaderNodeFactory", reader, "Python-derived route facts"),
        ("Classify route (#2)", "Rule Engine", "org.knime.base.node.rules.engine.RuleEngineNodeFactory", rule_model("knime_classification", CLASSIFICATION_RULES), "Infer route classification"),
        ("Assign severity (#3)", "Rule Engine", "org.knime.base.node.rules.engine.RuleEngineNodeFactory", rule_model("knime_severity", SEVERITY_RULES), "Infer decision priority"),
        ("CSV Writer (#4)", "CSV Writer", "org.knime.base.node.io.csvwriter.CSVWriterNodeFactory", writer_model(), "Export decisions.csv"),
    ]
    root = ET.Element(f"{{{NS}}}config", {"key": "workflow.knime"})
    for key, value in {"created_by": "5.12.0.v202606180846", "created_by_nightly": False,
                       "version": "5.1.0", "name": "LoopGuard Friendship Fair", "state": "IDLE"}.items():
        entry(root, key, value)
    cfg(root, "workflow_credentials")
    cfg(root, "annotations")
    nodes = cfg(root, "nodes")
    for index, (folder, name, factory, model, label) in enumerate(specs, 1):
        settings = node(factory, name, copy.deepcopy(model), label)
        annotation = settings.find(f"{{{NS}}}config[@key='nodeAnnotation']")
        for key, value in {"x-coordinate": 35 + (index - 1) * 240, "y-coordinate": 245}.items():
            annotation.find(f"{{{NS}}}entry[@key='{key}']").set("value", str(value))
        if index == 1:
            creation = cfg(settings, "node_creation_config")
            cfg(creation, "File System Connection")
            cfg(creation, "Data Table")
        write_xml(settings, destination / folder / "settings.xml")
        item = cfg(nodes, f"node_{index}")
        for key, value in {"id": index, "node_settings_file": folder + "/settings.xml",
                           "node_is_meta": False, "node_type": "NativeNode",
                           "ui_classname": "org.knime.core.node.workflow.NodeUIInformation"}.items():
            entry(item, key, value)
        bounds = cfg(cfg(item, "ui_settings"), "extrainfo.node.bounds")
        entry(bounds, "array-size", 4)
        for num, value in enumerate((70 + (index - 1) * 240, 180, 100, 80)):
            entry(bounds, str(num), value)
    connections = cfg(root, "connections")
    for index in range(1, 4):
        connection = cfg(connections, f"connection_{index - 1}")
        for key, value in {"sourceID": index, "destID": index + 1,
                           "sourcePort": 1, "destPort": 1}.items():
            entry(connection, key, value)
    write_xml(root, destination / "workflow.knime")
    return destination


def archive_workflow(workflow: Path, archive: Path) -> None:
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted(workflow.rglob("*")):
            if path.is_file() and not path.name.endswith(".lck"):
                bundle.write(path, str(Path(workflow.name) / path.relative_to(workflow)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a portable native KNIME workflow using installed node configuration formats.\n\nCSV Reader settings follow KNIME 5.12's saved schema. Rule Engine and legacy\nCSV Writer settings correspond to the factories shipped in KNIME Base/Javasnippet.\nNative execution validation is recorded separately in README.md; generating XML\nalone does not certify an executable workflow.\n")
    parser.add_argument("facts_csv", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--archive", type=Path)
    args = parser.parse_args()
    result = build_workflow(args.destination, args.facts_csv)
    if args.archive:
        archive_workflow(result, args.archive)
    print(result)
