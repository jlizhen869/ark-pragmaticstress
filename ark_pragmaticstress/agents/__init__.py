from .baseline_agent import BaselineAgent
from .policy_aware_agent import PolicyAwareAgent
from .variant_sensitive_agent import VariantSensitiveAgent

AGENT_REGISTRY = {
    "baseline": BaselineAgent,
    "policy_aware": PolicyAwareAgent,
    "variant_sensitive": VariantSensitiveAgent,
}
