"""Pure structural slicing validation; also usable by a standalone inspector."""
import copy
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
    require(plan == normalize(plan), 'Noncanonical slicing collection order')
    require(plan['parent'] == parent, 'Slicing parent identity mismatch')
    references(plan['rationale'], manifest, blobs)
    if plan['decision'] == 'no_split':
        require(not any(plan[k] for k in ('children','allocations','prerequisites','parent_final_checks')),
                'NO SPLIT must retain the direct parent route without child records')
        return plan
    require(2 <= len(plan['children']) <= 8, 'SPLIT requires 2–8 independently observable children')
    children = indexed(plan['children'], 'child')
    requirements = {r['id']:r for r in contract['requirements']}
    criteria = {}
    for child in children.values():
        for row in indexed(child['requirements'], 'criterion').values():
            supported(row, requirements, manifest, blobs)
            require(row['plan_state'] == 'gap' if row['gap_reason'] is not None else row['plan_state'] == 'planned',
                    'Gap criterion requires explicit gap_reason; planned evidence cannot claim a gap away')
            for rid in row['parent_requirement_ids']:
                require(set(requirements[rid]['boundaries']) <= set(row['boundaries']), 'Parent boundaries omitted from child')
            criteria[(child['id'],row['id'])] = row
    checks = indexed(plan['parent_final_checks'], 'parent check')
    for row in checks.values(): supported(row, requirements, manifest, blobs)
    allocations = {row['parent_requirement_id']:row for row in plan['allocations']}
    ordered_unique([r['parent_requirement_id'] for r in plan['allocations']], 'allocation IDs')
    require(allocations.keys() == requirements.keys(), 'Every parent R requires exactly one allocation')
    accounted, check_links = set(), set()
    for rid, allocation in allocations.items():
        ordered_unique(allocation['parent_check_ids'], 'parent check references')
        require(all(i in checks and rid in checks[i]['parent_requirement_ids'] for i in allocation['parent_check_ids']),
                'Missing/unrelated final parent ownership')
        check_links.update((rid,i) for i in allocation['parent_check_ids'])
        owners = allocation['contributors']
        require(bool(owners) == (allocation['parent_only_reason'] is None), 'Parent-only allocation requires an explicit integrated-owner reason')
        qualified = [(r['child_id'],r['criterion_id']) for r in owners]
        ordered_unique(qualified, 'qualified contributors')
        for ref in owners:
            key = (ref['child_id'],ref['criterion_id'])
            require(key in criteria and rid in criteria[key]['parent_requirement_ids'], 'Dangling/unrelated contribution')
            row = criteria[key]
            if ref['role'] == 'full':
                parent_row = requirements[rid]
                require(children[key[0]]['kind'] == 'outcome' and row['parent_requirement_ids'] == [rid]
                        and row['contribution'] == parent_row['statement'] and row['oracle'] == parent_row['oracle']
                        and {canonical(r) for r in row['source_refs']} == {canonical(r) for r in parent_row['source_refs']},
                        'Full mapping requires the complete original outcome and oracle; use partial/preservation for fragments')
            if children[key[0]]['kind'] == 'enabling':
                require(ref['role'] == 'preservation', 'Enabling steps cannot count as fulfilled product outcomes')
            accounted.add((rid,key))
    require(accounted == {(rid,key) for key,row in criteria.items() for rid in row['parent_requirement_ids']},
            'Orphan/unallocated child criterion')
    require(check_links == {(rid,i) for i,row in checks.items() for rid in row['parent_requirement_ids']},
            'Orphan parent final check')
    graph = {i:[] for i in children}
    edges = [(r['child_id'],r['requires_child_id']) for r in plan['prerequisites']]
    ordered_unique(edges, 'prerequisites')
    for edge in plan['prerequisites']:
        child, prerequisite = edge['child_id'], edge['requires_child_id']
        require(child in children and prerequisite in children and child != prerequisite, 'Missing/self prerequisite')
        require(edge['required_outcome'] == children[prerequisite]['outcome'], 'Prerequisite must name the exact observable child outcome')
        references(edge, manifest, blobs)
        graph[child].append(prerequisite)
    visiting, visited = set(), set()
    def visit(child):
        require(child not in visiting, 'Cyclic prerequisites')
        if child in visited: return
        visiting.add(child)
        for prerequisite in graph[child]: visit(prerequisite)
        visiting.remove(child); visited.add(child)
    for child in children: visit(child)
    return plan


def ordered_unique(values, label):
    require(len(values) == len(set(values)) and values == sorted(values), 'Duplicate or noncanonical ordering: '+label)


def indexed(rows, label):
    ordered_unique([r['id'] for r in rows], label+' IDs')
    return {r['id']:r for r in rows}


def supported(row, requirements, manifest, blobs):
    ids = row['parent_requirement_ids']
    ordered_unique(ids, 'parent requirement references')
    require(set(ids) <= requirements.keys(), 'Invented parent obligation')
    references(row, manifest, blobs)
    allowed = {canonical(ref) for rid in ids for ref in requirements[rid]['source_refs']}
    quoted = {canonical(ref) for ref in row['source_refs']}
    require(quoted <= allowed, 'Unrelated source support for child/parent check')
    require(all(quoted & {canonical(ref) for ref in requirements[rid]['source_refs']} for rid in ids),
            'Every attributed parent obligation needs actual source support')


def normalize(plan):
    """Canonicalize unordered proposal collections; never alter binding prose."""
    validate(plan,SLICING)
    result=copy.deepcopy(plan)
    result['children'].sort(key=lambda r:r['id'])
    result['allocations'].sort(key=lambda r:r['parent_requirement_id'])
    result['prerequisites'].sort(key=lambda r:(r['child_id'],r['requires_child_id']))
    result['parent_final_checks'].sort(key=lambda r:r['id'])
    cited=[result['rationale']]+result['prerequisites']+result['parent_final_checks']
    for child in result['children']:
        child['requirements'].sort(key=lambda r:r['id'])
        cited.extend(child['requirements'])
        for row in child['requirements']:row['boundaries'].sort()
    for row in cited:
        refs=row['source_refs']
        require(len({canonical(r) for r in refs})==len(refs),'Duplicate source citation')
        refs.sort(key=canonical)
        if 'parent_requirement_ids' in row:row['parent_requirement_ids'].sort()
    for row in result['allocations']:
        row['parent_check_ids'].sort()
        row['contributors'].sort(key=lambda r:(r['child_id'],r['criterion_id']))
    return result
