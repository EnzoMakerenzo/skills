from pathlib import Path

import pytest

from chat_analyse.features import (
    extract_features,
    find_skill_calls,
    find_skill_reads,
    normalize_skill_name,
    shorten_text,
)
from chat_analyse.load import Conversation, parse_conversations, read_export

SAMPLE_EXPORT = Path(__file__).parent / "data" / "sample_export.json"


def _sample_chats() -> list[Conversation]:
    return parse_conversations(read_export(SAMPLE_EXPORT)).conversations


@pytest.mark.parametrize(
    ("raw_name", "expected"),
    [
        ("anthropic-skills:projekt-codex", "projekt-codex"),
        ("ESP32:esp32", "esp32"),
        ("python-codex", "python-codex"),
        (" git-codex ", "git-codex"),
    ],
)
def test_normalize_skill_name_with_prefix_returns_plain_name(raw_name: str, expected: str) -> None:
    assert normalize_skill_name(raw_name) == expected


def test_shorten_text_long_text_ends_with_ellipsis() -> None:
    assert shorten_text("abcdef", 4) == "abc…"


def test_shorten_text_short_text_keeps_text_on_one_line() -> None:
    assert shorten_text("a\n  b", 10) == "a b"


def test_shorten_text_limit_below_one_raises_value_error() -> None:
    with pytest.raises(ValueError, match="mindestens 1"):
        shorten_text("abc", 0)


def test_find_skill_calls_sample_returns_normalized_names() -> None:
    blocks = [block for message in _sample_chats()[0].messages for block in message.content]
    assert find_skill_calls(blocks) == ["projekt-codex", "python-codex"]


def test_find_skill_reads_installed_paths_counts_only_installed_skills() -> None:
    blocks = [block for message in _sample_chats()[1].messages for block in message.content]
    assert find_skill_reads(blocks) == ["docx", "git-codex"]


def test_find_skill_calls_empty_input_returns_nothing() -> None:
    assert find_skill_calls([]) == []
    assert find_skill_reads([]) == []


def test_find_skill_calls_missing_input_is_ignored() -> None:
    assert find_skill_calls([{"type": "tool_use", "name": "Skill"}]) == []


def test_extract_features_with_summary_leaves_first_request_empty() -> None:
    features = extract_features(_sample_chats()[0])
    assert features.first_request == ""
    assert features.tool_uses == {"Skill": 2, "Bash": 1}
    assert features.month == "2026-01"


def test_extract_features_without_summary_uses_first_request() -> None:
    features = extract_features(_sample_chats()[1])
    assert features.first_request == "Mach ein Word-Dokument"
    assert features.skill_calls == ["esp32"]


def test_extract_features_long_summary_is_shortened() -> None:
    chat = _sample_chats()[2]
    long_chat = Conversation(
        uuid=chat.uuid,
        title=chat.title,
        summary="x" * 1000,
        created_at=chat.created_at,
        messages=chat.messages,
    )
    assert len(extract_features(long_chat).summary) == 400
