from enum import StrEnum


class EventDomain(StrEnum):
    PERSONA = "persona"
    WORKSPACE = "workspace"
    MARKET = "market"
    SCENARIO = "scenario"
    DECISION = "decision"
    EXECUTION = "execution"
    REVIEW = "review"
    SYSTEM = "system"


CANONICAL_EVENT_DOMAINS = frozenset(domain.value for domain in EventDomain)
