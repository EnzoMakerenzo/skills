from pathlib import Path

from chat_analyse.counts import count_usage
from chat_analyse.features import extract_features
from chat_analyse.load import parse_conversations, read_export

SAMPLE_EXPORT = Path(__file__).parent / "data" / "sample_export.json"


def test_count_usage_sample_counts_calls_reads_and_chats() -> None:
    conversations = parse_conversations(read_export(SAMPLE_EXPORT)).conversations
    counts = count_usage([extract_features(conversation) for conversation in conversations])
    assert counts.chat_count == 3
    assert counts.skill_calls_total == 3
    assert counts.skill_reads_total == 2
    assert counts.chats_with_skill == 2
    assert counts.first_date == "2026-01-15"
    assert counts.last_date == "2026-02-20"
    assert counts.uses_by_month == {
        "2026-01": {"projekt-codex": 1, "python-codex": 1},
        "2026-02": {"docx": 1, "git-codex": 1, "esp32": 1},
    }


def test_count_usage_empty_input_returns_zero_counts() -> None:
    counts = count_usage([])
    assert counts.chat_count == 0
    assert counts.first_date is None
    assert counts.uses_by_skill == {}
