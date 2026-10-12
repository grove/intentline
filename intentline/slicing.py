"""Pure structural slicing validation; also usable by a standalone inspector."""
import re
import unicodedata

if __package__:
    from .native_inspect import canonical, parse, sha, require, references
else:
    from native_inspect import canonical, parse, sha, require, references


def obj(properties):
    return {'type': 'object', 'properties': properties, 'required': list(properties), 'additionalProperties': False}


def arr(items, minimum=0, maximum=256):
    return {'type': 'array', 'items': items, 'minItems': minimum, 'maxItems': maximum}


TEXT = {'type': 'string', 'minLength': 1, 'maxLength': 4096}
DIGEST = {'type': 'string', 'pattern': '^[0-9a-f]{64}$'}
NULL_DIGEST = {'anyOf': [DIGEST, {'type': 'null'}]}
RID = {'type': 'string', 'pattern': '^R[1-9][0-9]{0,5}$'}
SID = {'type': 'string', 'pattern': '^S[1-9][0-9]{0,5}$'}
CID = {'type': 'string', 'pattern': '^C[1-9][0-9]{0,5}$'}
IID = {'type': 'string', 'pattern': '^I[1-9][0-9]{0,5}$'}
REF = obj({'source_id': SID, 'line_start': {'type':'integer','minimum':1,'maximum':999999},
           'line_end': {'type':'integer','minimum':1,'maximum':999999}, 'quote': TEXT})
REFS = arr(REF, 1, 64)
PARENT = obj({'contract_id': {'type':'string','pattern':'^[a-z0-9][a-z0-9-]{0,79}$'},
              'revision': {'type':'integer','minimum':1,'maximum':999999},
              'contract_sha256': DIGEST, 'source_bundle_sha256': DIGEST,
              'source_chain_sha256': DIGEST, 'continuity_sha256': NULL_DIGEST})
CRITERION = obj({'id': CID, 'parent_requirement_ids': arr(RID,1), 'contribution': TEXT,
                 'boundaries': arr(TEXT), 'seam': TEXT, 'oracle': TEXT,
                 'planned_evidence': TEXT, 'plan_state': {'enum':['planned','gap']},
                 'gap_reason': {'anyOf':[TEXT,{'type':'null'}]}, 'source_refs': REFS})
CHILD = obj({'id': SID, 'outcome': TEXT, 'kind': {'enum':['outcome','enabling']},
             'inheritance': {'const':'all_parent_constraints_and_exclusions'},
             'requirements': arr(CRITERION,1)})
CONTRIBUTOR = obj({'child_id': SID, 'criterion_id': CID,
                   'role': {'enum':['full','partial','preservation']}})
ALLOCATION = obj({'parent_requirement_id': RID, 'contributors': arr(CONTRIBUTOR,0,64),
                  'parent_check_ids': arr(IID,1), 'parent_only_reason': {'anyOf':[TEXT,{'type':'null'}]}})
CHECK = obj({'id': IID, 'parent_requirement_ids': arr(RID,1), 'owner': TEXT,
             'observable': TEXT, 'oracle': TEXT, 'planned_evidence': TEXT,
             'source_refs': REFS})
EDGE = obj({'child_id': SID, 'requires_child_id': SID, 'required_outcome': TEXT,
            'reason': TEXT, 'source_refs': REFS})
SLICING = obj({'record': {'const':'intentline.slicing'}, 'schema_version': {'const':1},
               'parent': PARENT, 'decision': {'enum':['no_split','split']},
               'rationale': obj({'why_not_one_delivery': TEXT, 'why_these_boundaries': TEXT,
                                  'basis': {'const':'advisory_plan_not_proof'}, 'source_refs': REFS,
                                  'uncertainties': arr(TEXT), 'next_action': TEXT}),
               'children': arr(CHILD,0,8), 'allocations': arr(ALLOCATION),
               'prerequisites': arr(EDGE,0,56), 'parent_final_checks': arr(CHECK),
               'supersedes_sha256': NULL_DIGEST})


def validate(value, schema, path='$'):
    if 'anyOf' in schema:
        for choice in schema['anyOf']:
            try: validate(value, choice, path)
            except ValueError: continue
            return
        raise ValueError(path + ': invalid nullable field')
    kind = schema.get('type')
    types = {'object':dict,'array':list,'string':str,'integer':int,'null':type(None)}
    require(not kind or type(value) is types[kind], path + ': wrong type')
    if 'const' in schema:
        require(type(value) is type(schema['const']) and value == schema['const'], path + ': unsupported constant')
    if 'enum' in schema: require(value in schema['enum'], path + ': unsupported value')
    if kind == 'object':
        require(set(value) == set(schema['properties']), path + ': missing or unexpected fields')
        for key, child in value.items(): validate(child, schema['properties'][key], path + '.' + key)
    elif kind == 'array':
        require(schema['minItems'] <= len(value) <= schema['maxItems'], path + ': row limit')
        for index, child in enumerate(value): validate(child, schema['items'], f'{path}[{index}]')
    elif kind == 'string':
        require(value.strip() and len(value) <= schema.get('maxLength',4096), path + ': empty/overlong text')
        require(not any(unicodedata.category(c) in ('Cc','Cf','Cs') and c not in '\n\r\t' for c in value), path + ': unsafe Unicode/control text')
        if 'pattern' in schema: require(re.fullmatch(schema['pattern'],value), path + ': invalid identifier/digest')
    elif kind == 'integer':
        require(schema['minimum'] <= value <= schema['maximum'], path + ': integer limit')


def parent_identity(contract, manifest, continuity_sha256=None):
    return {'contract_id':contract['contract_id'], 'revision':contract['revision'],
            'contract_sha256':sha(canonical(contract)), 'source_bundle_sha256':sha(canonical(manifest)),
            'source_chain_sha256':sha(canonical({'source_manifest':manifest,'ancestors':manifest.get('ancestors',[])})),
            'continuity_sha256':continuity_sha256}


def check(plan, contract, manifest, blobs, parent):
    validate(plan, SLICING)
    require(plan['parent'] == parent, 'Slicing parent identity mismatch')
    references(plan['rationale'], manifest, blobs)
    require(plan['decision'] == 'no_split', 'SPLIT validation is not available in this package')
    require(not any(plan[k] for k in ('children','allocations','prerequisites','parent_final_checks')),
            'NO SPLIT must retain the direct parent route without child records')
    return plan
