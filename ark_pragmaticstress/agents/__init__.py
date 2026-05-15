from .baseline_agent import BaselineAgent
from .policy_aware_agent import PolicyAwareAgent
from .variant_sensitive_agent import VariantSensitiveAgent
from .openai_agent import OpenAIAgent
from .openai_naive_agent import OpenAINaiveAgent

AGENT_REGISTRY = {
    "baseline": BaselineAgent,
    "policy_aware": PolicyAwareAgent,
    "variant_sensitive": VariantSensitiveAgent,
    "scaffold_policy_aware": OpenAIAgent,
    "scaffold_naive": OpenAINaiveAgent,
}
