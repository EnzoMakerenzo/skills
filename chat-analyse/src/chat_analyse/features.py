"""Merkmale je Chat: Werkzeuge, genutzte Skills und gekürzte Beschreibung."""

import json
import re
from collections import Counter
from collections.abc import Iterable, Iterator
from dataclasses import dataclass

from chat_analyse.load import ContentBlock, Conversation

SUMMARY_MAX_CHARACTERS = 400
FIRST_REQUEST_MAX_CHARACTERS = 300
SKILL_TOOL_NAME = "Skill"
USER_SENDER = "human"

# Nur installierte Skills zählen als Nutzung. Eine SKILL.md in einem Arbeitsordner oder
# Repository wird bearbeitet, nicht genutzt.
INSTALLED_SKILL_FILE = re.compile(
    r"(?:/mnt/skills|/\.claude/skills)/(?:[^\"\s/]+/)*?([^/\"\s]+)/SKILL\.md"
)


@dataclass(frozen=True)
class ChatFeatures:
    """Merkmalsblatt eines Chats für die Musterbildung."""

    uuid: str
    created_date: str
    month: str
    message_count: int
    title: str
    summary: str
    first_request: str
    tool_uses: dict[str, int]
    skill_calls: list[str]
    skill_reads: list[str]


def normalize_skill_name(raw_name: str) -> str:
    """Entfernt Präfixe wie "anthropic-skills:" oder "ESP32:" vom Skillnamen.

    Args:
        raw_name: Name, wie er im Werkzeugaufruf steht.

    Returns:
        Name nach dem letzten Doppelpunkt, ohne Leerraum am Rand.
    """
    return raw_name.rsplit(":", maxsplit=1)[-1].strip()


def shorten_text(text: str, max_characters: int) -> str:
    """Kürzt Text auf eine Höchstlänge und fasst Leerraum zusammen.

    Args:
        text: Ausgangstext.
        max_characters: Höchstzahl an Zeichen, mindestens 1.

    Returns:
        Text in einer Zeile; gekürzter Text endet mit "…".

    Raises:
        ValueError: Wenn max_characters kleiner als 1 ist.
    """
    if max_characters < 1:
        raise ValueError(f"max_characters muss mindestens 1 sein, erhalten: {max_characters}")
    single_line = " ".join(text.split())
    if len(single_line) <= max_characters:
        return single_line
    return single_line[: max_characters - 1] + "…"


def find_skill_calls(blocks: Iterable[ContentBlock]) -> list[str]:
    """Liefert die Skills, die über das Werkzeug Skill geladen wurden.

    Args:
        blocks: Inhaltsblöcke eines Chats.

    Returns:
        Normalisierte Skillnamen, je Aufruf ein Eintrag.
    """
    calls = []
    for block in _tool_uses(blocks):
        skill_name = _tool_input(block).get("skill")
        if block.get("name") == SKILL_TOOL_NAME and isinstance(skill_name, str):
            calls.append(normalize_skill_name(skill_name))
    return calls


def find_skill_reads(blocks: Iterable[ContentBlock]) -> list[str]:
    """Liefert die Skills, deren installierte SKILL.md direkt gelesen wurde.

    Args:
        blocks: Inhaltsblöcke eines Chats.

    Returns:
        Skillnamen, je Fundstelle ein Eintrag.
    """
    reads = []
    for block in _tool_uses(blocks):
        tool_input_text = json.dumps(_tool_input(block), ensure_ascii=False)
        reads.extend(INSTALLED_SKILL_FILE.findall(tool_input_text))
    return reads


def count_tool_uses(blocks: Iterable[ContentBlock]) -> dict[str, int]:
    """Zählt die Werkzeugaufrufe je Werkzeugname.

    Args:
        blocks: Inhaltsblöcke eines Chats.

    Returns:
        Anzahl Aufrufe je Werkzeug, absteigend sortiert.
    """
    tool_names = Counter(str(block.get("name", "")) for block in _tool_uses(blocks))
    return dict(tool_names.most_common())


def extract_features(conversation: Conversation) -> ChatFeatures:
    """Erstellt das Merkmalsblatt eines Chats.

    Args:
        conversation: Geprüfter Chat.

    Returns:
        Merkmalsblatt; die erste Anfrage steht nur dort, wo eine Zusammenfassung fehlt.
    """
    blocks = [block for message in conversation.messages for block in message.content]
    first_request = ""
    if not conversation.summary:
        first_request = shorten_text(_first_user_text(conversation), FIRST_REQUEST_MAX_CHARACTERS)
    return ChatFeatures(
        uuid=conversation.uuid,
        created_date=conversation.created_at.date().isoformat(),
        month=conversation.created_at.strftime("%Y-%m"),
        message_count=len(conversation.messages),
        title=conversation.title,
        summary=shorten_text(conversation.summary, SUMMARY_MAX_CHARACTERS),
        first_request=first_request,
        tool_uses=count_tool_uses(blocks),
        skill_calls=find_skill_calls(blocks),
        skill_reads=find_skill_reads(blocks),
    )


def _tool_uses(blocks: Iterable[ContentBlock]) -> Iterator[ContentBlock]:
    """Filtert die Blöcke mit Werkzeugaufrufen."""
    return (block for block in blocks if block.get("type") == "tool_use")


def _tool_input(block: ContentBlock) -> ContentBlock:
    """Liefert die Eingabe eines Werkzeugaufrufs, oder ein leeres Objekt."""
    tool_input = block.get("input")
    return tool_input if isinstance(tool_input, dict) else {}


def _first_user_text(conversation: Conversation) -> str:
    """Liefert den Text der ersten Nachricht des Nutzers, oder einen leeren Text."""
    for message in conversation.messages:
        if message.sender == USER_SENDER and message.text:
            return message.text
    return ""
