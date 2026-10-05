---
name: "sprach-codex"
description: "Sorgt dafür, dass jede Programmiersprache einen Codex hat: vorhandenen verwenden oder neuen nach Vorlage entwerfen und vorschlagen. Verwenden bei Code in einer Sprache ohne eigenen Codex. Nicht verwenden, wenn ein Codex der Sprache existiert, etwa python-codex, und nicht für YAML, JSON oder Markdown. Vorrang: Fach-Skills wie ESP32 gelten zusätzlich und ersetzen den Codex nicht."
---

# Sprach-Codex: ein Codex je Programmiersprache

## Zweck

Regeln zur Codequalität hängen von der Sprache ab. Statt für jede Sprache im Voraus einen Codex zu schreiben, stellt dieser Skill sicher, dass vor dem ersten Code in einer Sprache ein Codex vorhanden ist: Ein vorhandener wird verwendet, ein fehlender wird nach fester Vorlage entworfen und zur Speicherung vorgeschlagen.

In keiner Sprache wird stillschweigend nach Gutdünken gearbeitet. Entweder gilt ein Codex, oder es gelten ausdrücklich die gemeinsamen Grundsätze unten.

## Ablauf

| Schritt | Handlung |
|---|---|
| 1 | Sprachen des Vorhabens bestimmen: aus dem Entwurf oder, bei bestehenden Vorhaben, aus Dateiendungen und Build-Dateien |
| 2 | Je Sprache in der Liste der verfügbaren Skills nach `<sprache>-codex` suchen |
| 3 | Codex vorhanden: laden und anwenden |
| 4 | Codex fehlt: nach der Vorlage unten entwerfen, zur Speicherung vorschlagen und die entworfenen Regeln sofort anwenden |
| 5 | Enzo mitteilen: welcher Codex neu ist, auf welchen Quellen er beruht und dass er nur gespeichert dauerhaft gilt |

### Namensschema

| Sprache | Skill |
|---|---|
| Python | `python-codex` |
| C | `c-codex` |
| C++ | `cpp-codex` |
| Swift | `swift-codex` |
| SQL | `sql-codex` |
| Shell | `bash-codex` |
| andere | `<sprache>-codex`, kleingeschrieben, ohne Sonderzeichen |

### Wann kein eigener Codex entsteht

- Konfigurations- und Auszeichnungssprachen (YAML, JSON, Markdown) bekommen keinen Codex.
- Eine Nebensprache mit weniger als etwa 50 Zeilen im Vorhaben bekommt keinen eigenen Codex. Für sie gelten die gemeinsamen Grundsätze, und das wird in der Antwort gesagt.

## Gemeinsame Grundsätze

Dieser Kern gilt in jeder Sprache. Jeder Codex übernimmt ihn und übersetzt ihn in die Mittel der Sprache.

- Namen sagen, was ein Wert bedeutet. Physikalische Größen tragen die Einheit im Namen.
- Eine Funktion erledigt eine Aufgabe. Richtwerte: höchstens 30 Anweisungen, höchstens 4 Parameter, Verschachtelung höchstens 3 Ebenen.
- Keine booleschen Schalterparameter, die das Verhalten umschalten.
- Berechnung und Ein-/Ausgabe sind getrennt.
- Keine magischen Zahlen, kein veränderlicher globaler Zustand.
- Fehler werden nie stillschweigend geschluckt. Eingaben werden früh geprüft, Fehlermeldungen nennen den erhaltenen Wert und die Erwartung.
- Tests decken Normalfall, leere Eingabe, Grenzwerte und ungültige Eingabe ab.
- Kommentare erklären das Warum, nicht das Was.
- Was ein Werkzeug erzwingen kann, erzwingt das Werkzeug.
- Vor jeder Übergabe läuft die Abschlussprüfung, und ihr Ergebnis wird wörtlich berichtet.

## Vorlage für einen neuen Codex

`python-codex` ist die Referenz für Aufbau, Strenge und Ton. Er wird vor dem Entwerfen gelesen. Ein neuer Codex hat diese Abschnitte:

| Abschnitt | Inhalt |
|---|---|
| Zweck | wofür die Regeln da sind, Vorrang bestehender Konventionen |
| Werkzeuge | Formatierer, statische Prüfung, Warnungen des Übersetzers oder Typprüfung, Tests, je mit Aufruf und Grundkonfiguration |
| Benennung | Schreibweisen der Sprache, Einheiten, Sprache der Bezeichner |
| Funktionen | Grenzwerte, Parameter, Rückgaben |
| Struktur | Aufteilung in Dateien und Module, Abhängigkeitsrichtung |
| Typen und Speicher | Typsystem, Besitz und Lebensdauer, wo die Sprache das verlangt |
| Fehlerbehandlung | das Fehlermodell der Sprache und wie es zu verwenden ist |
| Besonderheiten | Eigenheiten von Sprache und Zielplattform |
| Tests | Rahmenwerk, Benennung, Pflichtfälle |
| Kommentare und Dokumentation | Form der Dokumentationskommentare |
| Abhängigkeiten | Paketverwaltung, festgeschriebene Versionen |
| Beispiel | ein Paar aus schlechtem und gutem Code |
| Abschlussprüfung | nummerierte Befehle |
| Herkunft der Regeln | Quellen je Regelgruppe |

## Anforderungen an den Inhalt

- Grundlage sind anerkannte Leitlinien der Sprache, etwa die offizielle Stilrichtlinie oder verbreitete Kernrichtlinien, nicht eigene Vorlieben. Die Quellen stehen im Abschnitt "Herkunft der Regeln".
- Werkzeuge und ihre Konfiguration werden aktuell nachgeschlagen, wenn in der Sitzung eine Suche verfügbar ist. Sonst wird im Codex gekennzeichnet, dass die Angaben aus dem Wissensstand des Assistenten stammen und zu prüfen sind.
- Nur prüfbare Regeln mit Grenzwerten. Die Richtwerte der gemeinsamen Grundsätze werden übernommen, damit alle Sprachen gleich streng sind.
- Löst die Sprache etwas anders als Python, gilt die Gepflogenheit der Sprache.
- Die Zielplattform bestimmt den Inhalt mit: C für einen Mikrocontroller verlangt andere Regeln als C für einen Rechner, zum Beispiel zu dynamischem Speicher, Unterbrechungsroutinen und Zeitverhalten.
- Gibt es einen passenden Fach-Skill, zum Beispiel für ESP32, verweist der Codex auf ihn, statt dessen Inhalt zu kopieren.
- Bezeichner auf Englisch, Kommentare auf Deutsch, wie in `python-codex`.
- Umfang etwa 120 bis 200 Zeilen.
- Die Beschreibung nennt die Sprache und den Anlass: "Verwenden bei jedem Schreiben, Ändern oder Prüfen von <Sprache>-Code."

## Speichern und Pflegen

- Der neue Codex wird Enzo als Vorschlag zur Speicherung vorgelegt. Ein Skill wird nie ohne seine Bestätigung gespeichert.
- Kann in der Sitzung kein Vorschlag vorgelegt werden, wird der vollständige Text ausgegeben und gesagt, dass er nicht gespeichert ist.
- Bis zur Speicherung gilt der Entwurf nur in der laufenden Sitzung.
- Ein vorhandener Codex wird nur auf Enzos Wunsch geändert, und dann als vollständige neue Fassung vorgeschlagen.
- Zeigt sich bei der Arbeit, dass eine Regel fehlt oder nicht trägt, wird das im Abschluss des Vorhabens als Änderungsvorschlag für den Codex notiert.