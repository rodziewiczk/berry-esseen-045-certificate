"""Exact domain/inequality joins for ALREADY REPLAYED C5 parent results.

These helpers neither execute parents nor authenticate historical receipts.
Only a controller which has actually observed their guarded replay may use
them in a fresh proof composition. They check numerical implication, not just
the presence of a status. No all-index or fresh-arithmetic flag is produced.
"""
from dataclasses import dataclass
from fractions import Fraction as F


def need(ok,message):
    if not ok: raise ValueError(message)


def rational(value):
    need(type(value) is str,'Exact rational text, never a floating-point premise')
    return F(value)


@dataclass(frozen=True)
class BoundFact:
    kind: str
    n: int
    rho_lower: F
    rho_upper: F
    radius: F
    upper: F | None
    receipt_sha256: str

    def __post_init__(self):
        need(self.kind in ('support','HIGH','owncap'),'Declared mathematical parent kind')
        need(type(self.n) is int and self.n == 5,'Same literal sample size5')
        need(all(type(x) is F for x in (self.rho_lower,self.rho_upper,self.radius)),
             'Exact rational domain bounds')
        need(1 <= self.rho_lower <= self.rho_upper and self.radius > 0,'Valid closed parent domain')
        need(self.upper is None if self.kind == 'support' else type(self.upper) is F and self.upper >= 0,
             'Support implication or nonnegative exact scalar bound')
        need(type(self.receipt_sha256) is str and len(self.receipt_sha256) == 64 and
             all(c in '0123456789abcdef' for c in self.receipt_sha256),'Concrete parent receipt identity')


def support_facts(result,pin):
    need(result.get('status') in ('PASS_FRESH_LITERAL5_Q0_SUPPORT9','PASS_FRESH_LITERAL5_Q0_SUPPORT_A0')
         and type(result.get('n')) is int and result['n'] == 5 and result.get('q') == '0'
         and result.get('K') == '0','Original same-law sharp-predecessor support implication')
    facts = []
    for row in result['rows']:
        need(row.get('status') == 'CONDITIONAL_SUPPORT_PASS' and type(row.get('n')) is int
             and row['n'] == 5 and len(row['rho']) == 2,'Complete original support row')
        facts.append(BoundFact('support',5,*map(rational,row['rho']),rational(row['radius']),None,pin))
    return facts


def high_facts(result,pin):
    need(result.get('status') in ('PASS_FRESH_LITERAL5_SUPPORTED_HIGH3',
                                  'PASS_FRESH_LITERAL5_SUPPORTED_ETA_HIGH4')
         and type(result.get('n')) is int and result['n'] == 5,'Original complete supported HIGH result')
    facts = []
    for row in result['rows']:
        need(type(row.get('n')) is int and row['n'] == 5,'Literal parent HIGH exponent')
        upper,cap = rational(row['upper']),rational(row['cap'])
        need(upper < cap,'Original strict HIGH cap')
        facts.append(BoundFact('HIGH',5,F(1),rational(row['rho_upper']),
                               rational(row['support_radius']),upper,pin))
    return facts


def owncap_facts(result,pin):
    need(result.get('status') in ('PASS_FRESH_LITERAL5_SUPPORTED_OWNCAPS3',
                                  'PASS_FRESH_LITERAL5_EXTENDED_SUPPORTED_B3_OWNCAP')
         and type(result.get('n')) is int and result['n'] == 5,'Original complete supported owncap result')
    facts = []
    for row in result['bands']:
        upper,cap = rational(row['exact_upper']),rational(row['cap'])
        need(upper < cap,'Original strict supported owncap')
        facts.append(BoundFact('owncap',5,*map(rational,row['rho']),
                               rational(row['support_absolute_upper']),upper,pin))
    return facts


@dataclass(frozen=True)
class GlobalOwncapFact:
    upper: F
    receipt_sha256: str

    def __post_init__(self):
        need(type(self.upper) is F and 0 <= self.upper < F(429,1000),'Exact global coarse5 bound')
        need(type(self.receipt_sha256) is str and len(self.receipt_sha256) == 64 and
             all(c in '0123456789abcdef' for c in self.receipt_sha256),'Global parent receipt identity')


def entails_profile(profile,assumed_high,assumed_owncap,facts,global_owncap=None):
    """Check that the SAME arbitrary law in the child's domain meets its inputs."""
    need(type(profile.get('n')) is int and type(profile.get('nmax')) is int
         and profile['n'] == profile['nmax'] == 5,'Child literal actual exponent5')
    need(rational(profile['q_contact']) == 0,'Unchanged sharp predecessor contact allowance')
    low = rational(profile['invariants']['rho_lo'])
    high = rational(profile['invariants']['rho'])
    radius = rational(profile['radius'])
    need(1 <= low <= high and radius > 0,'Child closed moment domain')
    for side in ('radius_minus','radius_plus'):
        if side in profile:
            need(rational(profile[side]) == radius,
                 'The declared one-sided support radius agrees with the symmetric child domain')
    def domain(fact): return fact.n == 5 and fact.rho_lower <= low <= high <= fact.rho_upper
    support = next((f for f in facts if f.kind == 'support' and domain(f) and f.radius <= radius),None)
    need(support is not None,'Same-law necessary support on the WHOLE child moment interval')
    edges = [dict(kind='support',parent=support.receipt_sha256,
                  acquired_radius=str(support.radius),child_radius=str(radius))]
    for kind,requested in [('HIGH',rational(assumed_high)),('owncap',rational(assumed_owncap))]:
        if kind == 'owncap' and requested == F(429,1000):
            need(type(global_owncap) is GlobalOwncapFact and global_owncap.upper <= requested,
                 'The original 0.429 INITIAL premise requires its GLOBAL all-law replay')
            edges.append(dict(kind='global-owncap',parent=global_owncap.receipt_sha256,
                              actual_upper=str(global_owncap.upper),required_upper=str(requested),
                              domain='ALL_STANDARDIZED_LAWS_WITH_FINITE_THIRD_MOMENT'))
            continue
        parent = next((f for f in facts if f.kind == kind and domain(f)
                       and radius <= f.radius and f.upper <= requested),None)
        need(parent is not None,'Fresh '+kind+' bound on a containing same-n moment/support domain')
        edges.append(dict(kind=kind,parent=parent.receipt_sha256,
                          actual_upper=str(parent.upper),required_upper=str(requested),
                          parent_radius=str(parent.radius),child_radius=str(radius)))
    return dict(scope='EXACT_PARENT_IMPLICATION_CHECK_NOT_PARENT_REPLAY',edges=edges,
                assumed_C4_sharp_and_unrestricted_contact_theorem=True,
                whole_child_rho=[str(low),str(high)],all_index_conclusion_verified=False)


def global_coarse429(result):
    need(result.get('status') == 'PASS_INDEPENDENT_GLOBAL_AUXILIARY5_READBACK'
         and result.get('n') == [5] and type(result['n'][0]) is int
         and result.get('target') == '429/1000' and result.get('finite_rho') == ['1','19/10']
         and type(result.get('strips')) is int and type(result.get('exact_rows')) is int
         and result['strips'] == result['exact_rows'] == 87
         and type(result.get('negative_controls')) is int
         and result['negative_controls'] == 24,'Full independently replayed GLOBAL coarse input')
    upper = rational(result['uniform_upper'])
    need(upper < F(429,1000),'Strict all-law coarse bound, not a supported replacement')
    return upper


def same_initial_candidate(fresh_initial,expected_input_sha,expected_stages,
                           expected_status='PASS_FRESH_CONDITIONAL_FULL_INITIAL5_ACQUISITION'):
    """A pinned historical INITIAL status is NOT the parent of a new resource."""
    need(type(fresh_initial.get('n')) is int and fresh_initial['n'] == 5,'Same INITIAL literal n')
    need(fresh_initial.get('status') == expected_status,'Exact original full INITIAL result kind')
    need(fresh_initial.get('input_sha256') == expected_input_sha,'Same original full INITIAL candidate')
    need(type(fresh_initial.get('stages')) is int and fresh_initial['stages'] == expected_stages,
         'All original INITIAL transitions, not a prefix')
    need(type(fresh_initial.get('total_cells_per_stage')) is int
         and type(fresh_initial.get('panels')) is int
         and fresh_initial['total_cells_per_stage'] == 2592 and fresh_initial['panels'] == 100,
         'Complete moment-cell and p-panel cover')
    need(type(fresh_initial.get('final_active')) is int and type(fresh_initial.get('final_gap_active')) is int
         and 0 <= fresh_initial['final_active'] == fresh_initial['final_gap_active'] <= 2592,
         'Every active final moment cell has its gap license')
