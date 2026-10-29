"""Zählung der Skill- und Werkzeugnutzung über alle Chats."""

from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass

from chat_analyse.features import ChatFeatures


@dataclass(frozen=True)
class UsageCounts:
    """Exakte Zählungen über alle Chats eines Exports."""

    chat_count: int
    first_date: str | None
    last_date: str | None
    skill_calls_total: int
    skill_reads_total: int
    chats_with_skill: int
    uses_by_skill: dict[str, int]
    chats_by_skill: dict[str, int]
    tool_uses: dict[str, int]
    uses_by_month: dict[str, dict[str, int]]


def count_usage(chats: Sequence[ChatFeatures]) -> UsageCounts:
    """Zählt Nutzungen je Skill, Chats je Skill, Werkzeuge und Monate.

    Eine Nutzung ist ein Aufruf über das Werkzeug Skill oder ein direktes Lesen der
    installierten SKILL.md.

    Args:
        chats: Merkmalsblätter aller gültigen Chats.

    Returns:
        Zählungen, absteigend nach Häufigkeit sortiert; Datumsangaben None ohne Chats.
    """
    uses_by_skill: Counter[str] = Counter()
    chats_by_skill: Counter[str] = Counter()
    tool_uses: Counter[str] = Counter()
    uses_by_month: dict[str, Counter[str]] = {}
    for chat in chats:
        skill_uses = chat.skill_calls + chat.skill_reads
        uses_by_skill.update(skill_uses)
        chats_by_skill.update(set(skill_uses))
        tool_uses.update(chat.tool_uses)
        uses_by_month.setdefault(chat.month, Counter()).update(skill_uses)
    dates = sorted(chat.created_date for chat in chats)
    return UsageCounts(
        chat_count=len(chats),
        first_date=dates[0] if dates else None,
        last_date=dates[-1] if dates else None,
        skill_calls_total=sum(len(chat.skill_calls) for chat in chats),
        skill_reads_total=sum(len(chat.skill_reads) for chat in chats),
        chats_with_skill=sum(1 for chat in chats if chat.skill_calls or chat.skill_reads),
        uses_by_skill=dict(uses_by_skill.most_common()),
        chats_by_skill=dict(chats_by_skill.most_common()),
        tool_uses=dict(tool_uses.most_common()),
        uses_by_month={
            month: dict(counts.most_common()) for month, counts in sorted(uses_by_month.items())
        },
    )
