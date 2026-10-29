import json
import shutil
from pathlib import Path

import pytest

from chat_analyse.cli import main

SAMPLE_EXPORT = Path(__file__).parent / "data" / "sample_export.json"


def test_main_sample_writes_features_and_counts(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    export_path = tmp_path / "conversations.json"
    shutil.copy(SAMPLE_EXPORT, export_path)
    assert main([str(export_path)]) == 0
    output_dir = tmp_path / "auswertung"
    feature_lines = (output_dir / "merkmale.jsonl").read_text(encoding="utf-8").splitlines()
    counts = json.loads((output_dir / "zaehlung.json").read_text(encoding="utf-8"))
    assert len(feature_lines) == 3
    assert len(counts["skipped"]) == 4
    report = capsys.readouterr().out
    assert "Chats ausgewertet: 3" in report
    assert "Übersprungen: 4" in report


def test_main_output_inside_repository_is_refused(tmp_path: Path) -> None:
    (tmp_path / ".git").mkdir()
    export_path = tmp_path / "conversations.json"
    shutil.copy(SAMPLE_EXPORT, export_path)
    assert main([str(export_path)]) == 1
    assert not (tmp_path / "auswertung").exists()


def test_main_missing_export_returns_error(tmp_path: Path) -> None:
    assert main([str(tmp_path / "fehlt.json")]) == 1
