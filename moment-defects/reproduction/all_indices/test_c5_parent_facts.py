from copy import deepcopy
from fractions import Fraction as F
import unittest
from .c5_parent_facts import BoundFact,GlobalOwncapFact,entails_profile,same_initial_candidate,rational

PIN = '1'*64


class ParentImplicationTests(unittest.TestCase):
    def setUp(self):
        self.profile = dict(n=5,nmax=5,q_contact='0',radius='99/40',
                            invariants=dict(rho_lo='237/200',rho='6/5'))
        self.facts = [BoundFact('support',5,F(237,200),F(6,5),F(99,40),None,PIN),
                      BoundFact('HIGH',5,F(1),F(6,5),F(3),F(2,5),PIN),
                      BoundFact('owncap',5,F(237,200),F(6,5),F(99,40),F(103,250),PIN)]
    def test_stronger_cap_implies_historical_weaker_cap(self):
        result = entails_profile(self.profile,'409/1000','207/500',self.facts)
        self.assertEqual(len(result['edges']),3)
        self.assertFalse(result['all_index_conclusion_verified'])
    def test_wrong_sample_rejected(self):
        with self.assertRaises(ValueError): BoundFact('HIGH',True,F(1),F(2),F(3),F(1),PIN)
    def test_partial_rho_domain_cannot_cover_child(self):
        self.facts[1] = BoundFact('HIGH',5,F(1),F(119,100),F(3),F(2,5),PIN)
        with self.assertRaises(ValueError): entails_profile(self.profile,'409/1000','207/500',self.facts)
    def test_too_small_supported_high_domain_rejected(self):
        self.facts[1] = BoundFact('HIGH',5,F(1),F(6,5),F(2),F(2,5),PIN)
        with self.assertRaises(ValueError): entails_profile(self.profile,'409/1000','207/500',self.facts)
    def test_weaker_scalar_cannot_license_child(self):
        with self.assertRaises(ValueError): entails_profile(self.profile,'399/1000','207/500',self.facts)
    def test_supported_cap_does_not_license_another_moment_band(self):
        self.profile['invariants']['rho_lo'] = '1'
        with self.assertRaises(ValueError): entails_profile(self.profile,'409/1000','207/500',self.facts)
    def test_no_float_premises(self):
        with self.assertRaises(ValueError): rational(.414)
    def test_optional_one_sided_radii_cannot_change_support_domain(self):
        self.profile.update(radius_minus='99/40',radius_plus='99/40')
        entails_profile(self.profile,'409/1000','207/500',self.facts)
        for side in ('radius_minus','radius_plus'):
            bad = deepcopy(self.profile);bad[side] = '5/2'
            with self.subTest(side=side),self.assertRaises(ValueError):
                entails_profile(bad,'409/1000','207/500',self.facts)
    def test_same_parent_input_and_all_stages_required(self):
        result = dict(status='PASS_FRESH_CONDITIONAL_FULL_INITIAL5_ACQUISITION',n=5,input_sha256=PIN,stages=9,total_cells_per_stage=2592,
                      panels=100,final_active=17,final_gap_active=17)
        same_initial_candidate(result,PIN,9)
        for field,value in [('input_sha256','0'*64),('stages',4),('panels',99),('final_gap_active',16),
                            ('panels',100.0),('total_cells_per_stage',2592.0)]:
            bad = deepcopy(result);bad[field] = value
            with self.subTest(field=field),self.assertRaises(ValueError): same_initial_candidate(bad,PIN,9)
    def test_regional_bound_cannot_replace_required_global429(self):
        with self.assertRaisesRegex(ValueError,'GLOBAL'):
            entails_profile(self.profile,'409/1000','429/1000',self.facts)
        result = entails_profile(self.profile,'409/1000','429/1000',self.facts,
                                  GlobalOwncapFact(F(428,1000),PIN))
        self.assertEqual(result['edges'][-1]['kind'],'global-owncap')
