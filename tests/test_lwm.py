"""Chart invariants, fog of war, memory tiers, the day cycle.

SuperInstance — liquid-world-model.
Run:  python3 tests/run_tests.py
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lwm.dungeon import DungeonWorld
from lwm.dungeon_demo import run_demo
from lwm.engine import agent_view, scorer_truth
from lwm.model import Chart, LiquidModel
from lwm.tiers import COST_ESSENCE, COST_REFLEX, COST_TRUTH, recall


def obs(place, exits=None, contents=None, trust=1.0, event=None, holding=None):
    return {"place": place, "exits": exits or {}, "contents": contents or [],
            "holding": holding or [], "trust": trust, "event": event}


class TinyWorld:
    """One room, one permanently locked door. For cycle/tier tests."""

    def __init__(self):
        self.room = "a"
        self._event = None

    def observe(self):
        o = obs("a", exits={"east": {"through": None}}, event=self._event)
        self._event = None
        return o

    def actions(self):
        return ["east"]

    def step(self, action):
        self._event = "The east door is locked."
        return self.observe()

    def truth(self):
        return {"room": self.room}


class TestContract(unittest.TestCase):
    def test_agent_view_hides_truth(self):
        world = DungeonWorld()
        view = agent_view(world)
        self.assertFalse(hasattr(view, "truth"))
        self.assertEqual(scorer_truth(world)["room"], "entrance")


class TestUncharted(unittest.TestCase):
    def test_uncharted_enumeration(self):
        chart = Chart()
        chart.observe(obs("a", exits={"east": {"through": "b"},
                                      "north": {"through": None}}),
                      day=1, step=0)
        got = {(u["place"], u["direction"], u["status"])
               for u in chart.uncharted()}
        self.assertIn(("a", "east", "never-tried"), got)
        self.assertIn(("a", "north", "never-tried"), got)
        self.assertIn(("b", None, "believed-unvisited"), got)
        # Walk east into b: both the exit and the place leave the set.
        chart.observe(obs("b", exits={"west": {"through": "a"}}), day=1, step=1)
        chart.record_transition("a", "east", "b", obs("b"), day=1, step=1,
                                holding_before=[])
        got = {(u["place"], u["direction"], u["status"])
               for u in chart.uncharted()}
        self.assertNotIn(("a", "east", "never-tried"), got)
        self.assertNotIn(("b", None, "believed-unvisited"), got)
        self.assertIn(("a", "north", "never-tried"), got)


class TestDoubt(unittest.TestCase):
    def test_contradiction_surprise_and_append_only_history(self):
        chart = Chart()
        chart.observe(obs("a", contents=["mug"]), day=1, step=0)
        place = chart.places["a"]
        before = [dict(h) for h in place.history]
        entries = chart.observe(obs("a", contents=[]), day=1, step=1)
        surprises = [e for e in entries if e.get("surprise")]
        self.assertEqual(len(surprises), 1)
        self.assertEqual(surprises[0]["believed"], ["mug"])
        self.assertEqual(surprises[0]["observed"], [])
        self.assertEqual(place.belief_contents, [])
        # History is append-only: the old entries are an untouched prefix.
        self.assertEqual([dict(h) for h in place.history[:len(before)]],
                         before)
        self.assertGreater(len(place.history), len(before))

    def test_low_trust_lowers_confidence_without_rewriting(self):
        chart = Chart()
        chart.observe(obs("a", contents=["mug"]), day=1, step=0)
        place = chart.places["a"]
        conf_before = place.confidence
        entries = chart.observe(obs("a", contents=["something else"],
                                    trust=0.2), day=1, step=1)
        self.assertEqual(place.belief_contents, ["mug"])  # not rewritten
        self.assertLess(place.confidence, conf_before)   # doubted instead
        self.assertTrue(any(e["type"] == "distrusted" for e in entries))
        self.assertFalse(any(e.get("surprise") for e in entries))


class TestFog(unittest.TestCase):
    def test_fog_decays_and_reobservation_restores(self):
        chart = Chart()
        chart.observe(obs("a", contents=["x"]), day=1, step=0)
        self.assertFalse(chart.is_fogged("a", day=2))       # seen yesterday
        fresh = chart.effective_confidence("a", day=2)
        self.assertTrue(chart.is_fogged("a", day=3))        # two days gone
        fogged = chart.effective_confidence("a", day=3)
        self.assertLess(fogged, fresh)                      # decayed
        chart.observe(obs("a", contents=["x"]), day=3, step=0)  # seen again
        self.assertFalse(chart.is_fogged("a", day=3))
        self.assertGreaterEqual(chart.effective_confidence("a", day=3),
                                fresh)


class TestDayCycle(unittest.TestCase):
    def test_sleep_flushes_episode_keeps_chart(self):
        model = LiquidModel(TinyWorld(), seed=3)
        model.wake("test day")
        model.run_day(max_steps=3)
        charted = model.chart.rooms_charted()
        self.assertGreaterEqual(charted, 1)
        self.assertTrue(model.episode)
        model.dream()
        model.sleep()
        self.assertEqual(model.episode, [])                # presence flushed
        self.assertTrue(model.archive[1]["entries"])       # ledger keeps it
        self.assertEqual(model.chart.rooms_charted(), charted)  # essence kept


class TestTiers(unittest.TestCase):
    def _slept_model(self):
        model = LiquidModel(TinyWorld(), seed=3)
        model.wake("tier day")
        model.run_day(max_steps=3)   # walks into the locked door: a surprise
        model.dream()
        model.sleep()
        return model

    def test_cost_ordering(self):
        self.assertLess(COST_REFLEX, COST_ESSENCE)
        self.assertLess(COST_ESSENCE, COST_TRUTH)
        model = self._slept_model()
        _a, c = recall(model, {"kind": "surprise", "day": 1, "index": 0},
                       "truth")
        self.assertEqual(c, COST_TRUTH)

    def test_truth_carries_detail_essence_does_not(self):
        model = self._slept_model()
        essence_ans, _ = recall(model, {"kind": "surprise", "day": 1,
                                        "index": 0}, "essence")
        truth_ans, _ = recall(model, {"kind": "surprise", "day": 1,
                                      "index": 0}, "truth")
        self.assertIsInstance(truth_ans, dict)
        self.assertIn("step", truth_ans)                    # full record
        self.assertEqual(truth_ans["reason"], "The east door is locked.")
        self.assertIsInstance(essence_ans, str)             # distilled line
        self.assertNotIn("The east door is locked.", essence_ans)

    def test_reflex_and_essence_never_open_the_archive(self):
        model = self._slept_model()

        class ExplodingDict(dict):
            def get(self, *a, **k):
                raise AssertionError("archive opened")

            def __getitem__(self, *a, **k):
                raise AssertionError("archive opened")

            def __contains__(self, *a, **k):
                raise AssertionError("archive opened")

        model.archive = ExplodingDict()
        # Reflex answers (or declines) from the live episode alone.
        ans, cost = recall(model, {"kind": "surprise", "day": 1, "index": 0},
                           "reflex")
        self.assertEqual(cost, COST_REFLEX)
        self.assertIsInstance(ans, str)
        # Essence answers from distilled notes, archive untouched.
        ans, _ = recall(model, {"kind": "surprise", "day": 1, "index": 0},
                        "essence")
        self.assertIsInstance(ans, str)
        # Truth is the only route that opens it — and demonstrably does.
        with self.assertRaises(AssertionError):
            recall(model, {"kind": "surprise", "day": 1, "index": 0},
                   "truth")


class TestDeterminism(unittest.TestCase):
    def test_same_seed_identical_curve(self):
        import tempfile
        with tempfile.TemporaryDirectory() as t1, \
                tempfile.TemporaryDirectory() as t2:
            c1 = run_demo(days=3, seed=7, out=Path(t1), verbose=False)
            c2 = run_demo(days=3, seed=7, out=Path(t2), verbose=False)
        self.assertEqual(c1, c2)


if __name__ == "__main__":
    unittest.main()
