"""Focused checks for the v5 hybrid model. Run: python test_hybrid.py"""
import math, unittest
import numpy as np
from engine import *

def pol(name): return next(p for p in POLICIES if p.name == name)
CALM = Scenario("calm", "calm")

class HybridTests(unittest.TestCase):
    def test_mass_ledger_closes_every_policy_and_scenario(self):
        for sc in [CALM, Scenario("s", "s", hs=2.0), Scenario("c", "c", collector_out=(1, 3)), Scenario("d", "d", dir_shift_deg=-30)]:
            for p in POLICIES:
                r = run(sc, p, Params(), seed=2)
                self.assertLess(abs(r["ledger_err_kg"]), 1e-6, (sc.name, p.name))

    def test_deterministic_for_same_seed(self):
        a = run(CALM, pol("hybrid_adaptive_crew"), Params(), seed=7)
        b = run(CALM, pol("hybrid_adaptive_crew"), Params(), seed=7)
        self.assertEqual(a["screens"], b["screens"])

    def test_do_nothing_leaks_only_through_entrance_share(self):
        r = run(CALM, pol("none"), Params(), seed=3)
        expect = (ENTR_Y[1] - ENTR_Y[0]) / 300.0           # entrance width / bloom width
        self.assertAlmostEqual(r["screens"] / r["arrived"], expect, delta=0.06)
        self.assertEqual(r["collected"], 0.0)

    def test_bubble_alone_gives_no_exclusion(self):
        a = run(CALM, pol("none"), Params(), seed=3)
        b = run(CALM, pol("bubble_only"), Params(), seed=3)
        self.assertAlmostEqual(a["screens"], b["screens"], places=6)   # by model design: lift only helps the boom

    def test_zero_lift_makes_bubbles_irrelevant(self):
        par = Params(p_lift_max=0.0)
        a = run(CALM, pol("boom_only"), par, seed=4)
        b = run(CALM, pol("hybrid_fixed"), par, seed=4)
        self.assertAlmostEqual(a["screens"], b["screens"], places=6)

    def test_bubble_lift_helps_boom_when_lift_positive(self):
        a = run(CALM, pol("boom_only"), Params(p_lift_max=0.7), seed=4)
        b = run(CALM, pol("hybrid_fixed"), Params(p_lift_max=0.7), seed=4)
        self.assertLess(b["screens"], a["screens"])

    def test_adaptive_uses_no_air_when_no_bloom(self):
        r = run(Scenario("idle", "idle", rate_kg_h=0.0001), pol("hybrid_adaptive"), Params(), seed=1)
        self.assertEqual(r["air_kwh"], 0.0)
        self.assertGreater(run(Scenario("idle", "idle", rate_kg_h=0.0001), pol("hybrid_fixed"), Params(), seed=1)["air_kwh"], 0.0)

    def test_adaptive_uses_less_energy_than_fixed_in_calm(self):
        a = run(CALM, pol("hybrid_adaptive"), Params(), seed=5)["air_kwh"]
        f = run(CALM, pol("hybrid_fixed"), Params(), seed=5)["air_kwh"]
        self.assertLess(a, f)

    def test_blind_sensors_fail_safe_to_full_air(self):
        r = run(Scenario("b", "b", sensor_blind=True), pol("hybrid_adaptive"), Params(), seed=1)
        self.assertGreater(r["air_kwh"], 15.0)

    def test_storm_stops_air_and_stands_crew_down(self):
        r = run(Scenario("s", "s", hs=2.0), pol("hybrid_adaptive_crew"), Params(), seed=1)
        self.assertEqual(r["air_kwh"], 0.0); self.assertEqual(r["crew_h"], 0.0); self.assertEqual(r["crew"], 0.0)

    def test_crew_only_removes_mass_never_adds(self):
        a = run(CALM, pol("hybrid_adaptive"), Params(), seed=6)
        b = run(CALM, pol("hybrid_adaptive_crew"), Params(), seed=6)
        self.assertLessEqual(b["screens"], a["screens"] + 1e-9)
        self.assertGreater(b["crew"], 0)

    def test_crew_respects_capacity(self):
        r = run(CALM, pol("hybrid_adaptive_crew"), Params(crew_kg_h=100.0), seed=6)
        self.assertLessEqual(r["crew"], 100.0 * r["crew_h"] + 1e-6)

    def test_adaptive_boom_rate_limited(self):
        r = run(Scenario("d", "d", dir_shift_deg=30), pol("hybrid_adaptive"), Params(), seed=1)
        self.assertLessEqual(r["boom_deg_moved"], 1.0 * HOURS * 60 + 1e-6)
        self.assertGreater(r["boom_deg_moved"], 25.0)

    def test_collector_outage_does_not_lose_mass(self):
        r = run(Scenario("o", "o", collector_out=(1, 3)), pol("boom_only"), Params(), seed=1)
        self.assertLess(abs(r["ledger_err_kg"]), 1e-6)

    def test_segment_crossing_helper(self):
        import engine
        # path (0,0)->(2,0) crosses boom (1,-1)->(1,3) at (1,0): halfway along the path but 1/4 along the boom
        cr, u = engine._seg_cross(np.array([[0., 0.]]), np.array([[2., 0.]]), np.array([1., -1.]), np.array([1., 3.]))
        self.assertTrue(cr[0]); self.assertAlmostEqual(float(u[0]), 0.25)
        cr, _ = engine._seg_cross(np.array([[0., 0.]]), np.array([[0.5, 0.]]), np.array([1., -1.]), np.array([1., 3.]))
        self.assertFalse(cr[0])

    def test_guided_distance_follows_boom_geometry(self):
        # a cohort crossing near the pivot has farther to travel than one crossing near the boom end,
        # so retention must be lower near the pivot (esc_per_m large, no time term)
        par = Params(surface_frac0=1.0, esc_per_m=0.01, esc_per_h=0.0)
        r_pivot = run(Scenario("p", "p", y_range=(-38.0, -30.0)), pol("boom_only"), par, seed=1)
        r_end = run(Scenario("e", "e", y_range=(100.0, 110.0)), pol("boom_only"), par, seed=1)
        self.assertLess(r_pivot["collected"] / r_pivot["arrived"], r_end["collected"] / r_end["arrived"])

if __name__ == "__main__":
    unittest.main(verbosity=1)
