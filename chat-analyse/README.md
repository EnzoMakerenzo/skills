# chat-analyse

Wertet `conversations.json` aus einem claude.ai-Datenexport aus: exakte Zählung der Skill- und Werkzeugnutzung und ein Merkmalsblatt je Chat. Die Musterbildung und die Skill-Vorschläge beschreibt `SKILL.md`.

## Aufruf

```
PYTHONPATH=src python3 -m chat_analyse /pfad/zu/conversations.json
```

Ausgabe im Ordner `auswertung` neben dem Export: `zaehlung.json` und `merkmale.jsonl`. Ein Ausgabeordner in einem Git-Repository wird verweigert, weil die Dateien Chatinhalte enthalten.

Optionen: `--output-dir <ordner>`.

## Entwicklung

Python ab 3.10, nur Standardbibliothek. Prüfung nach `python-codex`:

```
ruff format . && ruff check . && mypy src && pytest
```

Testdaten unter `tests/data/` sind künstlich.
