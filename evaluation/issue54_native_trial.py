#!/usr/bin/env python3
"""Temporary issue #54 native Deliver qualification on an immutable code candidate.

Only runs in the explicitly triggered GitHub-hosted macOS experiment.
The trusted setup obtains the exact public issue body and creates one genuine,
UNAPPROVED single-S1 Intentline draft/export. Product source, checks and native
Proofline are frozen; the checks do not dispatch any coding model.
This is NOT independent fresh-agent implementation or a security certification.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time


ROOT = Path(os.environ["RUNNER_TEMP"]) / "intentline54-native"
ROOT.mkdir(mode=0o700, parents=True, exist_ok=True)
PRODUCT = Path(os.environ["GITHUB_WORKSPACE"]) / "product"
TOOL = Path(os.environ["GITHUB_WORKSPACE"]) / "tool"
CODE_SHA = "0fdabb996f94be5ffded5063551d65268ee1bf6f"
CODE_TREE = "97a8e757757462c5a4b3d83719057c2346e26979"
TOOL_SHA = "adc0eb21c17bc70310b5f231ba8a092ca0d7d4e4"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(name: str, payload) -> None:
    path = ROOT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True, timeout=30).strip()


def clean_product() -> None:
    porcelain = subprocess.check_output(
        ["git", "-C", str(PRODUCT), "status", "--porcelain", "--untracked-files=all"], timeout=30
    )
    if porcelain:
        raise RuntimeError("Frozen candidate checkout is dirty")


def call(name: str, argv: list[str], *, cwd: Path, timeout: int = 200):
    write_json(name + "-invocation.json", {"argv": argv, "cwd": str(cwd)})
    started = time.monotonic()
    try:
        output = subprocess.run(argv, cwd=cwd, timeout=timeout, capture_output=True, check=False)
    except subprocess.TimeoutExpired as error:
        (ROOT / (name + ".stdout")).write_bytes(error.stdout or b"")
        (ROOT / (name + ".stderr")).write_bytes(error.stderr or b"")
        write_json(name + "-result.json", {"timed_out": True, "elapsed_s": time.monotonic() - started})
        raise
    (ROOT / (name + ".stdout")).write_bytes(output.stdout)
    (ROOT / (name + ".stderr")).write_bytes(output.stderr)
    write_json(name + "-result.json", {
        "exit_code": output.returncode, "timed_out": False, "elapsed_s": time.monotonic() - started,
        "stdout_sha256": sha256(output.stdout), "stderr_sha256": sha256(output.stderr),
        "stdout_bytes": len(output.stdout), "stderr_bytes": len(output.stderr),
    })
    print(name, "exit", output.returncode,
          "stdout:", output.stdout.decode(errors="replace")[:1800],
          "stderr:", output.stderr.decode(errors="replace")[:1800], flush=True)
    return output


def cli(name: str, *args: str):
    result = call(name, [PYTHON, "-B", "-m", "intentline", *args], cwd=PRODUCT, timeout=120)
    if result.returncode != 0:
        raise RuntimeError(f"Intentline producer step {name} failed, status {result.returncode}")
    return json.loads(result.stdout)["data"]


if git(PRODUCT, "rev-parse", "HEAD") != CODE_SHA:
    raise RuntimeError("Wrong pinned coding candidate")
if git(PRODUCT, "rev-parse", "HEAD^{tree}") != CODE_TREE:
    raise RuntimeError("Wrong pinned candidate source tree")
if git(TOOL, "rev-parse", "HEAD") != TOOL_SHA:
    raise RuntimeError("Wrong Proofline revision")
clean_product()
PYTHON = str(Path(sys.executable).resolve())
CODEX = shutil.which("codex")
if not CODEX:
    raise RuntimeError("No native Codex executable")
if subprocess.check_output([CODEX, "--version"], text=True).strip() != "codex-cli 0.162.1":
    raise RuntimeError("Codex version not exactly 0.162.1")
if subprocess.check_output([PYTHON, "--version"], text=True).strip().split()[1].split(".")[:2] != ["3", "12"]:
    raise RuntimeError("Requires Python 3.12")

# Public issue was fetched outside the sandbox, in an approved trusted setup.
issue_json = ROOT / "issue54.json"
if not issue_json.is_file():
    raise RuntimeError("Source issue fetch missing")
issue = json.loads(issue_json.read_text(encoding="utf-8"))
if issue.get("number") != 54 or issue.get("state") != "open":
    raise RuntimeError("Unexpected issue source metadata")
body = issue.get("body")
if not isinstance(body, str) or not body.strip():
    raise RuntimeError("Missing complete issue body")
S1 = ROOT / "original"
S1.mkdir(mode=0o700)
source = S1 / "issue-54.md"
source.write_bytes(body.encode("utf-8"))
if source.read_bytes() != body.encode("utf-8"):
    raise RuntimeError("Source bytes changed during capture")
source_hash = sha256(source.read_bytes())
write_json("source-identity.json", {
    "repository": "grove/intentline", "issue": 54, "url": issue["html_url"],
    "title": issue["title"], "created_at": issue["created_at"], "updated_at": issue["updated_at"],
    "source_bytes": source.stat().st_size, "source_sha256": source_hash,
    "source_semantics": "complete current public issue body, not authenticated original edit history",
})

work = ROOT / "acceptance"
prep = cli("intentline-prepare", "prepare", "--source", str(source),
           "--root", str(S1), "--out", str(work), "--json")
digest = prep["source_bundle_sha256"]
lines = body.splitlines()
def source_ref(prefix):
    hits = [(i, value) for i, value in enumerate(lines, 1) if value.startswith(prefix)]
    if len(hits) != 1:
        raise RuntimeError(f"Source S1 reference ambiguous: {prefix} ({len(hits)})")
    line, value = hits[0]
    return {"source_id": "S1", "line_start": line, "line_end": line, "quote": value}


ref1 = source_ref("- **R1 — Human-readable version:**")
ref2 = source_ref("- **R2 — Machine-readable version:**")
preserve_ref = source_ref("- Keep currently documented subcommands")
draft = {
    "contract": "intentline.acceptance", "schema_version": 1,
    "contract_id": "intentline-cli-version-54", "revision": 1,
    "source_bundle_sha256": digest,
    "intended_outcome": "Allow humans and automation to ask Intentline for its exact running version.",
    "requirements": [
        {"id": "R1", "statement": "The real CLI prints its version as one human-readable line.",
         "basis": "request", "source_refs": [ref1], "boundaries": ["--version", "no work directory", "no stderr"],
         "seam": "python -B -m intentline --version",
         "oracle": "Process exit 0, stdout precisely intentline 0.5.0rc1 plus LF, empty stderr and no work artifact",
         "planned_evidence": "Independent real entrypoint subprocess test R1", "plan_state": "planned"},
        {"id": "R2", "statement": "The CLI version query returns the schema-1 JSON result in either global flag order.",
         "basis": "request", "source_refs": [ref2], "boundaries": ["--json --version", "--version --json", "no work directory"],
         "seam": "python -B -m intentline --json --version",
         "oracle": "Process exit 0, one valid intentline.result schema-1 JSON with command=version and data.version=0.5.0rc1, no stderr",
         "planned_evidence": "Independent real entrypoint subprocess test R2", "plan_state": "planned"},
    ],
    "constraints": [
        {"statement": "Keep existing CLI commands and JSON result/error formats intact.",
         "basis": "request", "scope": "Existing operations", "source_refs": [preserve_ref]},
    ],
    "out_of_scope": [],
    "open_decisions": [],
    "evidence_gaps": [],
    "change_notes": [{"revision": 1, "kind": "initial"}],
}
draft_file = ROOT / "initial-draft.json"
draft_file.write_text(json.dumps(draft, sort_keys=True, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
cli("intentline-propose", "propose", "--work", str(work), "--draft", str(draft_file), "--json")
cli("intentline-check", "check", "--work", str(work), "--json")
export = ROOT / "export"
export_meta = cli("intentline-export", "export", "--work", str(work),
                  "--format", "json", "--out", str(export), "--json")
if export_meta.get("authority") != "unapproved":
    raise RuntimeError("Unexpected approval of advisory draft")
if (export / "source-S1.txt").read_bytes() != source.read_bytes():
    raise RuntimeError("JSON producer export source differs from original S1")
before_export = {p.name: sha256(p.read_bytes()) for p in export.iterdir() if p.is_file()}

r1 = [PYTHON, "-B", "-m", "unittest", "tests.test_cli_version.VersionQueries.test_R1_human_version"]
r2 = [PYTHON, "-B", "-m", "unittest", "tests.test_cli_version.VersionQueries.test_R2_json_version"]
scenarios = [
    ("wrong-map", [r1], {"R1": [{"index": 0, "argv": r2}]}),
    ("r1-only", [r1], {"R1": [{"index": 0, "argv": r1}]}),
    ("r1-r2", [r1, r2], {"R1": [{"index": 0, "argv": r1}], "R2": [{"index": 1, "argv": r2}]}),
]
write_json("run-identity.json", {
    "host": platform.platform(), "machine": platform.machine(),
    "python": sys.version, "python_path": PYTHON, "codex": CODEX,
    "codex_sha256": sha256(Path(CODEX).resolve().read_bytes()),
    "codex_version": "codex-cli 0.162.1",
    "candidate_commit": CODE_SHA, "candidate_tree": CODE_TREE,
    "proofline_commit": TOOL_SHA, "issue_sha256": source_hash,
    "intentline_initial_authority": "unapproved", "full_requirement_coverage": "UNKNOWN",
    "fresh_agent_launched": False, "operator_wrote_candidate_directly": True,
    "github_run_id": os.environ.get("GITHUB_RUN_ID"), "workflow_revision": os.environ.get("GITHUB_SHA"),
})
summaries = {}
for label, checks, links in scenarios:
    write_json(f"{label}-checks.json", checks)
    write_json(f"{label}-links.json", links)
    output_path = ROOT / (label + "-record")
    argv = [
        PYTHON, "-B", str(TOOL / "proofline.py"), "check",
        "--repo", str(PRODUCT), "--source", str(export / "source-S1.txt"),
        "--intentline-export", str(export),
        "--checks", str(ROOT / (label + "-checks.json")),
        "--intentline-links", str(ROOT / (label + "-links.json")),
        "--seconds", "200", "--check-seconds", "40",
        "--output", str(output_path)
    ]
    completed = call(label, argv, cwd=TOOL, timeout=245)
    item = {"exit_code": completed.returncode}
    report_path = output_path / "report.json"
    if report_path.exists():
        report = json.loads(report_path.read_text(encoding="utf-8"))
        item["status"] = report.get("status")
        item["native_boundary"] = report.get("boundary", {}).get("assessment", {}).get("status")
        item["candidate_tree"] = report.get("candidate_tree")
        item["report_sha256"] = sha256(report_path.read_bytes())
        status = call(label + "-status",
            [PYTHON, "-B", str(TOOL / "proofline.py"), "status",
             str(report_path), "--show-source"], cwd=TOOL, timeout=70)
        item["status_readback_exit"] = status.returncode
    else:
        item["report_present"] = False
    summaries[label] = item

after_export = {p.name: sha256(p.read_bytes()) for p in export.iterdir() if p.is_file()}
if before_export != after_export:
    raise RuntimeError("Native check modified the original Intentline export")
clean_product()
write_json("export-sha256-before-after.json", {"before": before_export, "after": after_export})
write_json("native-summary.json", {
    "scenarios": summaries, "candidate_commit": CODE_SHA, "candidate_tree": CODE_TREE,
    "source_sha256": source_hash, "coverage_completeness": "UNKNOWN",
    "native_check_model_calls": 0, "fresh_agent_adoption": "NOT DEMONSTRATED",
    "acceptance_authority": "unapproved",
})
print("Real native outcomes:", json.dumps(summaries, indent=2), flush=True)
if summaries["wrong-map"]["exit_code"] != 1 or summaries["wrong-map"].get("report_present") is not False:
    raise RuntimeError("Wrong R/argv mapping did not fail closed before a report")
for name in ("r1-only", "r1-r2"):
    item = summaries[name]
    if not (item.get("exit_code") == 0 and item.get("status") == "CHECKS PASSED"
            and item.get("native_boundary") == "OBSERVED"
            and item.get("candidate_tree") == CODE_TREE
            and item.get("status_readback_exit") == 0):
        raise RuntimeError(f"Native selected-check scenario is not qualified: {name}: {item}")
