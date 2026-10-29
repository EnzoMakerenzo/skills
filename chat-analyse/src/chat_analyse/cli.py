"""Kommandozeile: Export einlesen, Merkmale und Zählung schreiben, Prüfbericht ausgeben."""

import argparse
import json
import sys
from collections.abc import Sequence
from dataclasses import asdict
from pathlib import Path

from chat_analyse.counts import UsageCounts, count_usage
from chat_analyse.features import ChatFeatures, extract_features
from chat_analyse.load import LoadResult, parse_conversations, read_export

DEFAULT_OUTPUT_FOLDER = "auswertung"
FEATURES_FILE = "merkmale.jsonl"
COUNTS_FILE = "zaehlung.json"


def main(argv: Sequence[str] | None = None) -> int:
    """Führt die Auswertung aus.

    Args:
        argv: Argumente ohne Programmnamen; None liest sys.argv.

    Returns:
        0 bei Erfolg, 1 bei ungültiger Eingabe oder unzulässigem Ausgabeordner.
    """
    arguments = _parse_arguments(argv)
    export_path: Path = arguments.export
    output_dir: Path = arguments.output_dir or export_path.parent / DEFAULT_OUTPUT_FOLDER
    repository_root = find_repository_root(output_dir)
    if repository_root is not None:
        print(
            f"Ausgabeordner {output_dir} liegt im Git-Repository {repository_root}; "
            "Auswertungen enthalten Chatinhalte und dürfen dort nicht liegen.",
            file=sys.stderr,
        )
        return 1
    try:
        load_result = parse_conversations(read_export(export_path))
    except (FileNotFoundError, ValueError) as error:
        print(f"Export nicht lesbar: {error}", file=sys.stderr)
        return 1
    chats = [extract_features(conversation) for conversation in load_result.conversations]
    counts = count_usage(chats)
    write_results(output_dir, chats, counts, load_result)
    print(format_check_report(counts, load_result, output_dir))
    return 0


def find_repository_root(path: Path) -> Path | None:
    """Sucht ein Git-Repository, in dem der Pfad liegt.

    Args:
        path: Pfad, der noch nicht existieren muss.

    Returns:
        Wurzel des Repositorys, oder None, wenn der Pfad in keinem liegt.
    """
    for candidate in [path.resolve(), *path.resolve().parents]:
        if (candidate / ".git").exists():
            return candidate
    return None


def write_results(
    output_dir: Path,
    chats: Sequence[ChatFeatures],
    counts: UsageCounts,
    load_result: LoadResult,
) -> None:
    """Schreibt Merkmalsblätter und Zählung in den Ausgabeordner.

    Args:
        output_dir: Zielordner; wird angelegt, wenn er fehlt.
        chats: Merkmalsblätter, eine Zeile je Chat in merkmale.jsonl.
        counts: Zählungen für zaehlung.json.
        load_result: Liefert die übersprungenen Chats für zaehlung.json.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    feature_lines = [json.dumps(asdict(chat), ensure_ascii=False) for chat in chats]
    (output_dir / FEATURES_FILE).write_text("\n".join(feature_lines) + "\n", encoding="utf-8")
    counts_record = {
        **asdict(counts),
        "skipped": [asdict(skipped) for skipped in load_result.skipped],
    }
    (output_dir / COUNTS_FILE).write_text(
        json.dumps(counts_record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def format_check_report(counts: UsageCounts, load_result: LoadResult, output_dir: Path) -> str:
    """Erstellt den Prüfbericht für die Kommandozeile.

    Args:
        counts: Zählungen.
        load_result: Liefert die übersprungenen Chats.
        output_dir: Ort der geschriebenen Dateien.

    Returns:
        Mehrzeiliger Bericht.
    """
    lines = [
        f"Chats ausgewertet: {counts.chat_count}",
        f"Zeitraum: {counts.first_date} bis {counts.last_date}",
        f"Übersprungen: {len(load_result.skipped)}",
        *(
            f"  Position {skipped.position} ({skipped.uuid or 'ohne Kennung'}): {skipped.reason}"
            for skipped in load_result.skipped
        ),
        f"Skill-Aufrufe: {counts.skill_calls_total}",
        f"Gelesene SKILL.md: {counts.skill_reads_total}",
        f"Chats mit Skill-Nutzung: {counts.chats_with_skill}",
        f"Ausgabe: {output_dir}",
    ]
    return "\n".join(lines)


def _parse_arguments(argv: Sequence[str] | None) -> argparse.Namespace:
    """Liest die Argumente der Kommandozeile."""
    parser = argparse.ArgumentParser(
        prog="chat-analyse",
        description="Wertet conversations.json aus einem claude.ai-Export aus.",
    )
    parser.add_argument("export", type=Path, help="Pfad zu conversations.json")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help=f"Ausgabeordner, Standard: Ordner '{DEFAULT_OUTPUT_FOLDER}' neben dem Export",
    )
    return parser.parse_args(argv)


if __name__ == "__main__":
    sys.exit(main())
