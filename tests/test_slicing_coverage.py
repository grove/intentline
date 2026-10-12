import copy

from intentline.contracts import propose
from intentline.errors import IntentlineError
from intentline.paths import Directory
from intentline.records import canonical
from intentline.slice_records import preview, subject
from tests.test_slicing_nosplit import SliceCase


def split_plan(parent, contract):
    from tests.test_slicing_nosplit import no_split
    refs=contract['requirements'][0]['source_refs']
    plan=no_split(parent,refs);plan['decision']='split'
    plan['rationale'].update(why_not_one_delivery='Public interface must remain compatible while validation changes',
                              why_these_boundaries='Observe compatibility separately before the rejecting transition; merging loses the staged checkpoint')
    for index,row in enumerate(contract['requirements'],1):
        sid=f'S{index}'
        criterion={'id':'C1','parent_requirement_ids':[row['id']],'contribution':row['statement'],
                   **{k:copy.deepcopy(row[k]) for k in ('boundaries','seam','oracle','planned_evidence','plan_state','source_refs')},
                   'gap_reason':None}
        plan['children'].append({'id':sid,'outcome':row['statement'],'kind':'outcome',
                                  'inheritance':'all_parent_constraints_and_exclusions','requirements':[criterion]})
        plan['parent_final_checks'].append({'id':f'I{index}','parent_requirement_ids':[row['id']],
                                            'owner':'Future assembled-product verifier','observable':row['statement'],
                                            'oracle':row['oracle'],'planned_evidence':'Observe one assembled public candidate including negative cases',
                                            'source_refs':copy.deepcopy(row['source_refs'])})
        plan['allocations'].append({'parent_requirement_id':row['id'],
                                    'contributors':[{'child_id':sid,'criterion_id':'C1','role':'full'}],
                                    'parent_check_ids':[f'I{index}'],'parent_only_reason':None})
    return plan


class CoverageCase(SliceCase):
    def setup_split(self):
        if not self.setup_work(): return False
        row=copy.deepcopy(self.draft['requirements'][0]);row.update(id='R2',statement='Keep valid usernames unchanged',
             source_refs=[{'source_id':'S1','line_start':2,'line_end':2,'quote':'Keep valid usernames unchanged'}],
             boundaries=['valid username'],oracle='Exact valid username retained',planned_evidence='Observe public validation with a valid username')
        self.draft['requirements'].append(row)
        self.draft['constraints']=[{'statement':'Preserve valid usernames','basis':'request','scope':'Every child', 'source_refs':copy.deepcopy(row['source_refs'])}]
        self.draft['out_of_scope']=[{'statement':'No other changes to valid usernames','source_refs':copy.deepcopy(row['source_refs'])}]
        propose(self.work,self.write_draft(self.draft))
        with Directory(self.work) as work:self.parent=subject(work)[-1]
        self.plan=split_plan(self.parent,self.draft);self.plan_path=self.root/'slice.json';self.save_plan()
        return True


class Coverage(CoverageCase):
    def test_complete_split_parent_unchanged_and_qualified_local_ids(self):
        if not self.setup_split(): return
        before=(self.work/'current.json').read_bytes()
        self.assertEqual(self.save_record()['status'],'SPLIT_PROPOSED')
        self.assertEqual(preview(self.work,self.plan_path)['semantics'],'unverified')
        self.assertEqual((self.work/'current.json').read_bytes(),before)
        self.assertEqual([c['requirements'][0]['id'] for c in self.plan['children']],['C1','C1'])

    def test_negative_coverage_mutants(self):
        if not self.setup_split(): return
        good=copy.deepcopy(self.plan)
        changes=[lambda p:p['allocations'].pop(), lambda p:p['allocations'].append(copy.deepcopy(p['allocations'][0])),
                 lambda p:p['children'][0].update(id='S2'),lambda p:p['children'][0].update(inheritance='none'),
                 lambda p:p['children'][0]['requirements'][0].update(parent_requirement_ids=['R99']),
                 lambda p:p['allocations'][0]['contributors'][0].update(criterion_id='C99'),
                 lambda p:p['parent_final_checks'][0].update(owner=''),lambda p:p['parent_final_checks'].pop(),
                 lambda p:p['children'][0]['requirements'][0].update(contribution='Only empty usernames'),
                 lambda p:p['children'][0]['requirements'][0].update(boundaries=[]),
                 lambda p:p['children'][0]['requirements'][0].update(source_refs=p['children'][1]['requirements'][0]['source_refs']),
                 lambda p:p['children'][0]['requirements'][0].update(plan_state='gap'),
                 lambda p:p['children'].reverse(),lambda p:p['children'][0].update(children=[])]
        for index,change in enumerate(changes):
            self.plan=copy.deepcopy(good);change(self.plan)
            with self.subTest(mutant=index),self.assertRaises(IntentlineError):preview(self.work,self.save_plan())

    def test_distributed_and_parent_only_obligations(self):
        if not self.setup_split(): return
        criterion=copy.deepcopy(self.plan['children'][0]['requirements'][0]);criterion['contribution']='Preserve the rejection invariant across the public interface'
        self.plan['children'][1]['requirements'].append({**criterion,'id':'C2'})
        self.plan['allocations'][0]['contributors'][0]['role']='partial'
        self.plan['allocations'][0]['contributors'].append({'child_id':'S2','criterion_id':'C2','role':'preservation'})
        self.assertEqual(preview(self.work,self.save_plan())['status'],'SPLIT_PROPOSED')
        self.plan['children'][1]['requirements'].pop()
        self.plan['allocations'][0]['contributors'].pop()
        self.plan['allocations'][1].update(contributors=[],parent_only_reason='Verify preserved valid behavior only on the assembled parent')
        self.plan['children'][1]['requirements']=[criterion]
        self.plan['allocations'][0]['contributors'].append({'child_id':'S2','criterion_id':'C1','role':'partial'})
        self.assertEqual(preview(self.work,self.save_plan())['status'],'SPLIT_PROPOSED')

    def test_enabling_gap_and_real_dependency_dag(self):
        if not self.setup_split(): return
        edge={'child_id':'S2','requires_child_id':'S1','required_outcome':self.plan['children'][0]['outcome'],
              'reason':'Transition needs the observable interface invariant','source_refs':self.plan['rationale']['source_refs']}
        self.plan['prerequisites']=[edge]
        self.plan['children'][0]['kind']='enabling'
        self.plan['allocations'][0]['contributors'][0]['role']='preservation'
        row=self.plan['children'][0]['requirements'][0];row.update(plan_state='gap',gap_reason='Public observation harness must be supplied')
        self.assertEqual(preview(self.work,self.save_plan())['status'],'SPLIT_PROPOSED')
        good=copy.deepcopy(self.plan)
        for edge_change in ('self','missing','ticket','cycle','duplicate'):
            self.plan=copy.deepcopy(good)
            if edge_change=='self':self.plan['prerequisites'][0]['requires_child_id']='S2'
            if edge_change=='missing':self.plan['prerequisites'][0]['requires_child_id']='S99'
            if edge_change=='ticket':self.plan['prerequisites'][0]['required_outcome']='Issue closed'
            if edge_change=='cycle':self.plan['prerequisites'].insert(0,{**edge,'child_id':'S1','requires_child_id':'S2','required_outcome':self.plan['children'][1]['outcome']})
            if edge_change=='duplicate':self.plan['prerequisites'].append(edge)
            with self.subTest(edge=edge_change),self.assertRaises(IntentlineError):preview(self.work,self.save_plan())

    def test_pinned_public_authored_fixture_both_routes(self):
        import json
        from pathlib import Path
        from intentline.sources import prepare
        from intentline.slice_records import record, status
        if not self.setup_work(): return
        fixture=Path(__file__).resolve().parents[1]/'examples/slicing'
        work=self.root/'public-work';captured=prepare(fixture/'request.md',[],fixture,work)
        contract=json.loads((fixture/'good.template.json').read_bytes());contract['source_bundle_sha256']=captured['source_bundle_sha256']
        propose(work,self.write_draft(contract))
        with Directory(work) as directory:parent=subject(directory)[-1]
        for kind in ('no-split','split'):
            plan=json.loads((fixture/(kind+'.template.json')).read_bytes());plan['parent']=parent
            if kind=='split':plan['supersedes_sha256']=status(work)['plan_sha256']
            path=self.root/'public-plan.json';path.write_bytes(canonical(plan))
            self.assertEqual(preview(work,path)['semantics'],'unverified')
            record(work,path,parent['contract_sha256'])
        self.assertEqual(status(work)['history_count'],2)
