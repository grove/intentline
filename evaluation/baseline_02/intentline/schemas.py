"""The supported schema subset is kept here and published as JSON Schema."""
import re

from .errors import IntentlineError
from .records import string


def obj(properties, required=None):
    return {'type': 'object', 'properties': properties, 'required': list(properties) if required is None else required,
            'additionalProperties': False}


def array(items, minimum=0):
    return {'type': 'array', 'items': items, 'minItems': minimum}


TEXT = {'type': 'string', 'minLength': 1}
DIGEST = {'type': 'string', 'pattern': '^[0-9a-f]{64}$'}
POSITIVE = {'type': 'integer', 'minimum': 1, 'maximum': 999999}
RID = {'type': 'string', 'pattern': '^R[1-9][0-9]*$'}
REF = obj({'source_id': {'type': 'string', 'pattern': '^S[1-9][0-9]*$'},
           'line_start': POSITIVE, 'line_end': POSITIVE, 'quote': TEXT})
REFS = array(REF, 1)
BASIS = {'type': 'string', 'enum': ['request', 'project_constraint', 'necessary_invariant']}
REQ = obj({'id': RID, 'statement': TEXT, 'basis': BASIS, 'source_refs': REFS,
           'boundaries': array(TEXT), 'seam': TEXT, 'oracle': TEXT, 'planned_evidence': TEXT,
           'plan_state': {'type': 'string', 'enum': ['planned', 'gap']}})
CONSTRAINT = obj({'statement': TEXT, 'basis': BASIS, 'source_refs': REFS, 'scope': TEXT})
EXCLUSION = obj({'statement': TEXT, 'source_refs': REFS})
DECISION = obj({'id': {'type': 'string', 'pattern': '^D[1-9][0-9]*$'}, 'statement': TEXT,
                'source_refs': REFS, 'kind': {'type': 'string', 'enum': ['outcome', 'authority_conflict']}})
GAP = obj({'requirement_ids': array(RID, 1), 'reason': TEXT})
MAPPING = obj({'from': array(RID, 1), 'to': array(RID), 'reason': TEXT})
NOTE = obj({'revision': POSITIVE, 'kind': {'type': 'string', 'enum': ['initial', 'revision']},
            'reason': TEXT, 'previous_contract_sha256': DIGEST, 'mappings': array(MAPPING),
            'retired_ids': array(RID), 'claimed_authority': TEXT}, ['revision', 'kind'])
ACCEPTANCE = obj({'contract': {'const': 'intentline.acceptance'}, 'schema_version': {'const': 1},
                  'contract_id': {'type': 'string', 'pattern': '^[a-z0-9][a-z0-9-]{0,79}$'},
                  'revision': POSITIVE, 'source_bundle_sha256': DIGEST, 'intended_outcome': TEXT,
                  'requirements': array(REQ, 1), 'constraints': array(CONSTRAINT),
                  'out_of_scope': array(EXCLUSION), 'open_decisions': array(DECISION),
                  'evidence_gaps': array(GAP), 'change_notes': array(NOTE, 1),
                  'advisory_notes': array(TEXT)},
                 ['contract', 'schema_version', 'contract_id', 'revision', 'source_bundle_sha256',
                  'intended_outcome', 'requirements', 'constraints', 'out_of_scope',
                  'open_decisions', 'evidence_gaps', 'change_notes'])


def validate(value, schema, path='$'):
    kind = schema.get('type')
    valid_types = {'object': dict, 'array': list, 'string': str, 'integer': int}
    if kind and type(value) is not valid_types[kind]:
        raise IntentlineError(f'{path}: expected {kind}')
    if 'const' in schema and (type(value) is not type(schema['const']) or value != schema['const']):
        raise IntentlineError(f'{path}: unsupported constant')
    if 'enum' in schema and value not in schema['enum']:
        raise IntentlineError(f'{path}: unsupported value')
    if kind == 'object':
        if set(value) - set(schema['properties']) or set(schema['required']) - set(value):
            raise IntentlineError(f'{path}: missing or unexpected fields')
        for key, child in value.items():
            validate(child, schema['properties'][key], path + '.' + key)
    elif kind == 'array':
        if len(value) < schema.get('minItems', 0):
            raise IntentlineError(f'{path}: too few rows')
        for i, child in enumerate(value):
            validate(child, schema['items'], f'{path}[{i}]')
    elif kind == 'string':
        string(value)
        if 'pattern' in schema and not re.fullmatch(schema['pattern'], value):
            raise IntentlineError(f'{path}: invalid identifier or digest')
    elif kind == 'integer':
        if not schema.get('minimum', value) <= value <= schema.get('maximum', value):
            raise IntentlineError(f'{path}: integer out of bounds')

FINDING = obj({'id': {'type':'string', 'pattern':'^A[1-9][0-9]*$'},
               'requirement_ids': array(RID), 'source_refs': REFS,
               'evidence': TEXT, 'consequence': TEXT, 'correction': TEXT})
AUDIT = obj({'record': {'const':'intentline.audit'}, 'schema_version': {'const':1},
             'contract_sha256': DIGEST, 'source_bundle_sha256': DIGEST,
             'actor': TEXT, 'timestamp': TEXT,
             'reported_independence': {'type':'string', 'enum':['self_check','unverified_independence','independent']},
             'authentication': {'const':'unverified'},
             'outcome': {'type':'string', 'enum':['READY_FOR_ADOPTION','CHANGES_NEEDED','BLOCKED']},
             'coverage': TEXT, 'findings': array(FINDING)})
APPROVAL = obj({'record': {'const':'intentline.approval'}, 'schema_version': {'const':1},
                'contract_sha256': DIGEST, 'source_bundle_sha256': DIGEST,
                'actor': TEXT, 'timestamp': TEXT, 'reference': TEXT,
                'record_bytes_utf8': TEXT},
               ['record','schema_version','contract_sha256','source_bundle_sha256','actor','timestamp','reference'])
ADOPTION = obj({'record': {'const':'intentline.adoption'}, 'schema_version': {'const':1},
                'contract_sha256': DIGEST, 'source_bundle_sha256': DIGEST,
                'actor': TEXT, 'timestamp': TEXT, 'reference': TEXT,
                'record_bytes_utf8': TEXT, 'assertion': {'const':'operator_asserted'},
                'authentication': {'const':'unverified'}, 'approval_file_sha256': DIGEST,
                'approval_file_bytes_utf8': TEXT, 'approval_file_path': TEXT,
                'approval_file_identity': obj({'device': {'type':'integer','minimum':0}, 'inode': {'type':'integer','minimum':0}})},
               ['record','schema_version','contract_sha256','source_bundle_sha256','actor','timestamp','reference',
                'assertion','authentication','approval_file_sha256','approval_file_bytes_utf8',
                'approval_file_path','approval_file_identity'])
