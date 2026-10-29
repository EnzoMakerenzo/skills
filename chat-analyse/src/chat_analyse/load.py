"""Einlesen und Prüfen der Datei conversations.json aus dem claude.ai-Export."""

import json
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, TypeAlias

# Inhaltsblöcke sind ungeprüftes JSON aus dem Export; ihr Aufbau hängt vom Blocktyp ab
# und wird erst in features.py gelesen.
ContentBlock: TypeAlias = dict[str, Any]


@dataclass(frozen=True)
class Message:
    """Eine Nachricht eines Chats."""

    sender: str
    text: str
    content: list[ContentBlock]


@dataclass(frozen=True)
class Conversation:
    """Ein geprüfter Chat aus dem Export."""

    uuid: str
    title: str
    summary: str
    created_at: datetime
    messages: list[Message]


@dataclass(frozen=True)
class SkippedConversation:
    """Ein Chat, der beim Einlesen übersprungen wurde."""

    position: int
    uuid: str | None
    reason: str


@dataclass(frozen=True)
class LoadResult:
    """Ergebnis des Einlesens: gültige Chats und übersprungene mit Grund."""

    conversations: list[Conversation]
    skipped: list[SkippedConversation]


def read_export(export_path: Path) -> list[object]:
    """Liest conversations.json und prüft, dass die Datei eine Liste enthält.

    Args:
        export_path: Pfad zur Datei conversations.json.

    Returns:
        Die Einträge der Datei, noch ungeprüft.

    Raises:
        FileNotFoundError: Wenn die Datei fehlt.
        ValueError: Wenn die Datei kein JSON oder keine Liste enthält.
    """
    try:
        raw_export = json.loads(export_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"{export_path} ist kein gültiges JSON: {error}") from error
    if not isinstance(raw_export, list):
        raise ValueError(
            f"{export_path} muss eine Liste von Chats enthalten, erhalten: "
            f"{type(raw_export).__name__}"
        )
    return raw_export


def parse_conversations(raw_export: Sequence[object]) -> LoadResult:
    """Überführt die Einträge des Exports in geprüfte Chats.

    Args:
        raw_export: Einträge aus read_export.

    Returns:
        Gültige Chats und übersprungene Chats mit Position, Kennung und Grund.
    """
    conversations: list[Conversation] = []
    skipped: list[SkippedConversation] = []
    for position, entry in enumerate(raw_export):
        parsed = _parse_entry(entry)
        if isinstance(parsed, Conversation):
            conversations.append(parsed)
        else:
            uuid = entry.get("uuid") if isinstance(entry, dict) else None
            skipped.append(
                SkippedConversation(
                    position=position,
                    uuid=uuid if isinstance(uuid, str) else None,
                    reason=parsed,
                )
            )
    return LoadResult(conversations=conversations, skipped=skipped)


def _parse_entry(entry: object) -> Conversation | str:
    """Prüft einen Eintrag; liefert den Chat oder den Grund, warum er fehlt."""
    if not isinstance(entry, dict):
        return f"Eintrag ist kein Objekt, sondern {type(entry).__name__}"
    uuid = entry.get("uuid")
    if not isinstance(uuid, str) or not uuid:
        return "Kennung uuid fehlt"
    created_at = _parse_timestamp(entry.get("created_at"))
    if created_at is None:
        return f"Zeitstempel created_at ungültig: {entry.get('created_at')!r}"
    raw_messages = entry.get("chat_messages")
    if not isinstance(raw_messages, list):
        return "Feld chat_messages fehlt oder ist keine Liste"
    if not raw_messages:
        return "Chat enthält keine Nachrichten"
    return Conversation(
        uuid=uuid,
        title=_as_text(entry.get("name")),
        summary=_as_text(entry.get("summary")),
        created_at=created_at,
        messages=[_parse_message(message) for message in raw_messages],
    )


def _parse_message(raw_message: object) -> Message:
    """Überführt eine Nachricht; fehlende Felder werden leer gesetzt."""
    if not isinstance(raw_message, dict):
        return Message(sender="", text="", content=[])
    raw_content = raw_message.get("content")
    content = (
        [block for block in raw_content if isinstance(block, dict)]
        if isinstance(raw_content, list)
        else []
    )
    return Message(
        sender=_as_text(raw_message.get("sender")),
        text=_as_text(raw_message.get("text")),
        content=content,
    )


def _parse_timestamp(value: object) -> datetime | None:
    """Liest einen Zeitstempel im ISO-Format mit Zeitzone; sonst None."""
    if not isinstance(value, str):
        return None
    # Python 3.10 liest die Endung "Z" für UTC noch nicht.
    normalized_value = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        timestamp = datetime.fromisoformat(normalized_value)
    except ValueError:
        return None
    # Ohne Zeitzone wäre die Zuordnung zu Tag und Monat mehrdeutig.
    return timestamp if timestamp.tzinfo is not None else None


def _as_text(value: object) -> str:
    """Liefert den Wert als Text, oder einen leeren Text für Fehlwerte."""
    return value if isinstance(value, str) else ""
