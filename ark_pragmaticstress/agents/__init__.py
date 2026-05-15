from .baseline_agent import BaselineAgent
from .policy_aware_agent import PolicyAwareAgent
from .variant_sensitive_agent import VariantSensitiveAgent
from .scaffold_policy_aware_agent import ScaffoldPolicyAwareAgent
from .scaffold_naive_agent import ScaffoldNaiveAgent

AGENT_REGISTRY = {
    "baseline": BaselineAgent,
    "policy_aware": PolicyAwareAgent,
    "variant_sensitive": VariantSensitiveAgent,
    "scaffold_policy_aware": ScaffoldPolicyAwareAgent,
    "scaffold_naive": ScaffoldNaiveAgent,
}
