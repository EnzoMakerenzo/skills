from pathlib import Path

import pytest

from chat_analyse.load import parse_conversations, read_export

SAMPLE_EXPORT = Path(__file__).parent / "data" / "sample_export.json"


def test_read_export_sample_returns_all_entries() -> None:
    assert len(read_export(SAMPLE_EXPORT)) == 7


def test_read_export_not_a_list_raises_value_error(tmp_path: Path) -> None:
    export_path = tmp_path / "conversations.json"
    export_path.write_text('{"uuid": "x"}', encoding="utf-8")
    with pytest.raises(ValueError, match="Liste"):
        read_export(export_path)


def test_read_export_invalid_json_raises_value_error(tmp_path: Path) -> None:
    export_path = tmp_path / "conversations.json"
    export_path.write_text("[{", encoding="utf-8")
    with pytest.raises(ValueError, match="kein gültiges JSON"):
        read_export(export_path)


def test_read_export_missing_file_raises_file_not_found(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        read_export(tmp_path / "fehlt.json")


def test_parse_conversations_sample_keeps_valid_chats() -> None:
    result = parse_conversations(read_export(SAMPLE_EXPORT))
    assert [chat.uuid for chat in result.conversations] == ["chat-a", "chat-b", "chat-c"]


def test_parse_conversations_sample_reports_each_skipped_chat_with_reason() -> None:
    result = parse_conversations(read_export(SAMPLE_EXPORT))
    reasons = {skipped.position: skipped.reason for skipped in result.skipped}
    assert set(reasons) == {3, 4, 5, 6}
    assert "kein Objekt" in reasons[3]
    assert "uuid fehlt" in reasons[4]
    assert "created_at ungültig" in reasons[5]
    assert "keine Nachrichten" in reasons[6]


def test_parse_conversations_skipped_chat_keeps_uuid_when_present() -> None:
    result = parse_conversations(read_export(SAMPLE_EXPORT))
    assert [skipped.uuid for skipped in result.skipped] == [None, None, "chat-zeit", "chat-leer"]


def test_parse_conversations_empty_export_returns_nothing() -> None:
    result = parse_conversations([])
    assert result.conversations == []
    assert result.skipped == []


def test_parse_conversations_missing_title_becomes_empty_text() -> None:
    result = parse_conversations(read_export(SAMPLE_EXPORT))
    assert result.conversations[2].title == ""
