"""One versioned stdout result; diagnostics use stderr."""

import argparse
import json
import os
import sys

from .errors import IntentlineError


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise IntentlineError(message)


def parser():
    p = Parser(description="Plan acceptance without implementing or proving it.")
    p.add_argument("--json", action="store_true", help="emit intentline.result schema 1")
    sub = p.add_subparsers(dest="command", required=True)
    for name in ("prepare", "propose", "check", "render", "status", "audit-record", "adopt", "export"):
        command = sub.add_parser(name)
        command.add_argument("--json", action="store_true", default=argparse.SUPPRESS)
        if name != "prepare":
            command.add_argument("--work", required=True)
        if name == "prepare":
            command.add_argument("--source", required=True)
            command.add_argument("--context", action="append", default=[])
            command.add_argument("--root", default=os.getcwd())
            command.add_argument("--out", default=".intentline/work/request")
        if name == "propose":
            command.add_argument("--draft", required=True)
        if name == "render":
            command.add_argument("--format", choices=["markdown"], default="markdown")
        if name == "audit-record":
            command.add_argument("--report", required=True)
        if name == "adopt":
            command.add_argument("--expected-contract-sha256", required=True)
            command.add_argument("--approval-file", required=True)
        if name == "export":
            command.add_argument("--format", choices=["proofline-direct", "markdown", "json"], required=True)
            command.add_argument("--out", required=True)
    return p


def execute(args):
    if args.command == "prepare":
        from .sources import prepare
        return prepare(args.source, args.context, args.root, args.out)
    if args.command == "propose":
        from .contracts import propose
        return propose(args.work, args.draft)
    if args.command in ("check", "status", "render"):
        from .contracts import inspect
        status, contract = inspect(args.work)
        if args.command == "render":
            if contract is None:
                raise IntentlineError("No current contract to render")
            from .render import markdown
            from .paths import Directory
            from .sources import bundle
            with Directory(args.work) as work:
                manifest, _, _ = bundle(work)
            status["markdown"] = markdown(contract, status, manifest)
        return status
    if args.command == "audit-record":
        from .audits import audit_record
        return audit_record(args.work, args.report)
    if args.command == "adopt":
        from .adoption import adopt
        return adopt(args.work, args.expected_contract_sha256, args.approval_file)
    raise IntentlineError("No work item recorded yet")


def main(argv=None):
    sys.dont_write_bytecode = True
    actual = sys.argv[1:] if argv is None else argv
    json_mode = "--json" in actual
    command = None
    try:
        args = parser().parse_args(actual)
        command = args.command
        data = execute(args)
        result = {"result": "intentline.result", "schema_version": 1,
                  "command": command, "ok": True, "data": data}
        code = data.get("exit_code", 0)
        result["ok"] = code == 0
        if json_mode:
            print(json.dumps(result, ensure_ascii=True, sort_keys=True))
        else:
            print(data.get("markdown", data.get("summary", json.dumps(data, ensure_ascii=True))))
        return code
    except (IntentlineError, OSError, UnicodeError, ValueError) as exc:
        code = exc.code if isinstance(exc, IntentlineError) else 3
        message = str(exc)
        print(message, file=sys.stderr)
        if json_mode:
            print(json.dumps({"result": "intentline.result", "schema_version": 1,
                              "command": command, "ok": False,
                              "error": {"code": code, "message": message}}, ensure_ascii=True))
        return code
