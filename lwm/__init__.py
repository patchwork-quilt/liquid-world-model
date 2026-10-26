"""liquid-world-model (lwm) — SuperInstance.

An engine-agnostic framework for liquid world models: an agent that
charts a world it has not finished learning, doubts its senses and
its beliefs, forgets on a day cycle after testifying, and remembers
through priced tiers. See engine.py for the contract, model.py for
the chart and the cycle, tiers.py for routed recall.
"""

from .engine import World, agent_view, scorer_truth
from .model import Chart, LiquidModel
from .policy import ExplorerPolicy
from .tiers import COST_ESSENCE, COST_REFLEX, COST_TRUTH, recall

__version__ = "0.1.0"
__all__ = [
    "World", "agent_view", "scorer_truth", "Chart", "LiquidModel",
    "ExplorerPolicy", "recall", "COST_REFLEX", "COST_ESSENCE", "COST_TRUTH",
]
