from .base import BasePersona, PersonaTurn
from .indirect_refusal import IndirectRefusalPersona
from .mitigated_request import MitigatedRequestPersona
from .persuasion_appeal import PersuasionAppealPersona

PERSONA_REGISTRY = {
    "indirect_refusal": IndirectRefusalPersona,
    "mitigated_request": MitigatedRequestPersona,
    "persuasion_appeal": PersuasionAppealPersona,
}
