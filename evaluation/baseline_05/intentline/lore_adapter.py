"""Experimental envelope inspection of an explicitly supplied Lore report."""
import argparse
import json
import sys

from .errors import IntentlineError
from .paths import read_file
from .records import parse, sha

PIN = '55ee9830e38fe869669376a089c9fbd4dddca43c'


def inspect_report(path):
    raw, _ = read_file(path)
    report = parse(raw)
    kind, mode, snapshot = 'unrecognized', None, None
    if isinstance(report, dict) and type(report.get('schema_version')) is int:
        if (report['schema_version'] == 1 and report.get('contract') == 'lore.bootstrap_context'
                and report.get('mode') == 'bootstrap_source_only'
                and isinstance(report.get('evidence'), list)
                and isinstance(report.get('source_snapshot_sha256'), str)
                and isinstance(report.get('discovery'), dict)
                and type(report.get('omitted_source_groups')) is int
                and isinstance(report.get('budget'), dict)):
            kind, mode = 'bootstrap_schema_1', report['mode']
            snapshot = {'source_snapshot_sha256': report['source_snapshot_sha256']}
        elif (report['schema_version'] == 5 and isinstance(report.get('snapshot'), dict)
              and all(isinstance(report['snapshot'].get(k), str) and report['snapshot'][k]
                      for k in ('project_id', 'registry_revision'))
              and isinstance(report.get('capabilities'), dict)
              and isinstance(report.get('intelligence'), dict)
              and isinstance(report['intelligence'].get('mode'), str)
              and isinstance(report.get('budget'), dict)):
            kind, mode, snapshot = 'initialized_schema_5', report['intelligence']['mode'], report['snapshot']
    return {'record': 'intentline.lore-inspection', 'schema_version': 1,
            'compatibility_revision': PIN, 'report_sha256': sha(raw), 'envelope': kind,
            'reported_mode': mode, 'reported_snapshot': snapshot,
            'authority': 'candidate_leads_only', 'freshness': 'unverified',
            'limitations': ['Envelope recognition is not full Lore schema/registry validation.',
                           'Read the entire original captured report; never discard lifecycle, scope, relationships, conflicts, omissions or grants.',
                           'Missing/deleted/stale original documentary witnesses remain evidence gaps.',
                           'Registry identity is retained evidence, not current checkout freshness; reversion does not revive old authority.',
                           'Fallback/static inspection/report status is not fresh inference, runtime proof or approval.',
                           'Unrecognized or incomplete reports remain ordinary untrusted context; normal planning continues.']}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report')
    args = parser.parse_args(argv)
    try:
        print(json.dumps(inspect_report(args.report), sort_keys=True))
        return 0
    except (IntentlineError, OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return exc.code if isinstance(exc, IntentlineError) else 3


if __name__ == '__main__':
    sys.exit(main())
