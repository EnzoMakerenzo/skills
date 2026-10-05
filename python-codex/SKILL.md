---
name: "python-codex"
description: "Regeln für sauberen Python-Code mit Grenzwerten, Werkzeugen und Abschlussprüfung. Verwenden bei jedem Schreiben, Ändern oder Prüfen von Python-Code."
---

# Python-Codex: Regeln für sauberen Code

## Zweck

Code wird öfter gelesen als geschrieben. Die Regeln zielen darauf, dass Enzo oder eine Kollegin den Code in einem Jahr ohne Rückfrage versteht und gefahrlos ändert. Grenzwerte sind Richtwerte: Eine Abweichung ist erlaubt, wenn sie in einer Zeile begründet wird.

Vorhandene Konventionen eines bestehenden Projekts haben Vorrang vor diesem Codex. Für das Vorgehen vor dem ersten Code gilt `projekt-codex`.

## Werkzeuge

| Aufgabe | Werkzeug | Aufruf |
|---|---|---|
| Formatierung | ruff | `ruff format .` |
| Statische Prüfung | ruff | `ruff check .` |
| Typprüfung | mypy | `mypy src` |
| Tests | pytest | `pytest` |

Was ein Werkzeug erzwingt, wird nicht von Hand diskutiert. Grundkonfiguration für `pyproject.toml`:

```toml
[tool.ruff]
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "N", "SIM", "C90", "PL", "RUF", "D"]

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["D", "PLR2004"]

[tool.ruff.lint.mccabe]
max-complexity = 10

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.lint.pylint]
max-args = 4
max-statements = 30

[tool.mypy]
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
```

## Benennung

- Namen sagen, was der Wert bedeutet, nicht welchen Typ er hat: `groundwater_level_m` statt `data2`.
- Ausgeschriebene Wörter. Ausnahmen: verbreitete Bibliothekskürzel (`np`, `pd`, `gpd`, `plt`) und Laufvariablen in Schleifen bis drei Zeilen.
- Physikalische Größen tragen die Einheit im Namen: `depth_cm`, `conductivity_us_per_cm`, `duration_s`.
- Funktionen heißen nach dem, was sie tun (Verb), Wahrheitswerte beginnen mit `is_`, `has_` oder `should_`.
- Bezeichner auf Englisch, Docstrings und Kommentare auf Deutsch.

## Funktionen

- Eine Funktion erledigt eine Aufgabe. Braucht die Beschreibung ein "und", wird geteilt.
- Richtwerte: höchstens 30 Anweisungen, höchstens 4 Parameter, Verschachtelung höchstens 3 Ebenen.
- Mehr als 4 zusammengehörige Parameter werden zu einer `dataclass`.
- Keine booleschen Schalterparameter, die das Verhalten umschalten. Stattdessen zwei Funktionen.
- Optionale Parameter nur als Schlüsselwortargumente (`*` in der Signatur).
- Frühe Rückgabe statt tiefer Verschachtelung.
- Berechnung und Ein-/Ausgabe trennen: Funktionen, die rechnen, lesen keine Dateien und schreiben keine.

## Struktur

- Quellcode unter `src/<paketname>/`, Tests unter `tests/`.
- Module bis etwa 300 Zeilen, ein Thema je Modul.
- Ein-/Ausgabe, Netzwerk und Datenbank am Rand, Fachlogik im Kern ohne Seiteneffekte.
- Keine veränderlichen globalen Zustände. Konfiguration an einer Stelle, als unveränderliche `dataclass`.
- Keine magischen Zahlen: benannte Konstanten mit Einheit.
- Pfade mit `pathlib.Path`, nie als zusammengesetzte Zeichenketten.

## Typen

- Typannotationen an allen Funktionen. `Any` nur mit Kommentar, warum es nötig ist.
- Fehlende Werte ausdrücklich als `X | None` und an genau einer Stelle behandeln.
- Daten an Systemgrenzen (Dateien, Schnittstellen) beim Einlesen prüfen und in typisierte Strukturen überführen.

## Fehlerbehandlung

- Nur bestimmte Ausnahmen fangen. Kein `except:` und kein `except Exception:` ohne erneutes Auslösen.
- Fehler nie stillschweigend schlucken. Übersprungene Datensätze werden gezählt und gemeldet.
- Fehlermeldungen nennen den erhaltenen Wert und die Erwartung.
- Früh scheitern: Eingaben am Anfang prüfen, nicht mitten in der Berechnung.
- `logging` statt `print` in allem, was kein Kommandozeilen-Einstiegspunkt ist.

## Daten und Reproduzierbarkeit

- Rohdaten werden nie überschrieben. Ergebnisse gehen in eigene Dateien.
- Koordinatenbezugssystem, Zeitzone und Einheit immer ausdrücklich setzen und prüfen, nie annehmen.
- Fehlwerte ausdrücklich behandeln und dokumentieren, wie.
- In pandas keine verkettete Zuweisung, sondern `.loc`.
- Zufallszahlen mit festem Startwert, Abhängigkeiten mit festgeschriebenen Versionen.

## Tests

- Jedes Arbeitspaket bringt seine Tests mit.
- Getestet wird Verhalten, nicht die innere Umsetzung.
- Testnamen: `test_<was>_<bedingung>_<erwartung>`.
- Pflichtfälle: Normalfall, leere Eingabe, Fehlwerte, Grenzwerte, ungültige Eingabe.
- Kein Netzwerk und keine echten Produktivdaten in Tests. Kleine Beispieldateien unter `tests/data/`.

## Kommentare und Dokumentation

- Kommentare erklären das Warum, nicht das Was.
- Docstrings im Google-Format für alle öffentlichen Funktionen, mit `Args`, `Returns`, `Raises`.
- Kein auskommentierter Code, keine Notiz ohne Kontext.

## Abhängigkeiten

- Standardbibliothek zuerst. Jede neue Abhängigkeit wird mit einem Satz begründet.
- Die Python-Version wird aus dem Projekt übernommen. In neuen Projekten die aktuelle stabile Version.

## Beispiel

Schlecht:

```python
def proc(d, f=True):
    r = []
    for x in d:
        if x[1] > 0:
            if f:
                r.append(x[1] * 0.01)
            else:
                r.append(x[1])
    return r
```

Gut:

```python
from collections.abc import Sequence

CENTIMETERS_PER_METER = 100


def depths_to_meters(depths_cm: Sequence[float]) -> list[float]:
    """Rechnet Abstichmaße von Zentimeter in Meter um.

    Args:
        depths_cm: Abstichmaße in Zentimeter, nicht negativ.

    Returns:
        Abstichmaße in Meter in gleicher Reihenfolge.

    Raises:
        ValueError: Wenn ein Abstichmaß negativ ist.
    """
    negative_depths = [depth for depth in depths_cm if depth < 0]
    if negative_depths:
        raise ValueError(f"Abstichmaß darf nicht negativ sein, erhalten: {negative_depths}")
    return [depth / CENTIMETERS_PER_METER for depth in depths_cm]
```

## Abschlussprüfung

Vor jeder Übergabe ausführen und das Ergebnis wörtlich berichten:

1. `ruff format .`
2. `ruff check .`
3. `mypy src`
4. `pytest`

Schlägt eine Prüfung fehl oder konnte sie nicht laufen, steht das in der ersten Zeile der Übergabe. Code wird nie als geprüft bezeichnet, wenn die Prüfung nicht gelaufen ist.