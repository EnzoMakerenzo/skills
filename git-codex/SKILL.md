---
name: "git-codex"
description: "Git-Regeln nach Software-Anwendungsentwicklung 2: Repository, Feature-Branches, Commit-Nachrichten, Review. Verwenden bei jedem neuen Programmiervorhaben und jeder Arbeit mit Git. Nicht verwenden bei reinen Fragen zu Git-Befehlen ohne Arbeit an einem Repository. Vorrang: gilt zusätzlich zu projekt-codex und dem Codex der Sprache; Konventionen eines vorhandenen Repositorys gehen vor."
---

# Git-Codex: Versionsverwaltung

## Zweck

Jede Änderung am Code soll nachvollziehbar, rückgängig zu machen und gesichert sein. Die Regeln folgen der Lehrveranstaltung Software-Anwendungsentwicklung 2 an der Fachhochschule Wiener Neustadt (Einheiten "Git" und "Projektplanung"), angepasst auf Vorhaben, bei denen der Assistent schreibt und Enzo prüft.

Bestehende Konventionen eines vorhandenen Repositorys haben Vorrang vor diesem Codex.

## Repository anlegen

Für jedes Programmiervorhaben wird ein Repository angelegt, auch für ein einzelnes Skript. Kein Code entsteht außerhalb eines Repositorys.

| Schritt | Befehl oder Handlung | Hinweis |
|---|---|---|
| 1 | `git init -b main` im Projektordner | Hauptbranch heißt `main` |
| 2 | `git config user.name` und `git config user.email` prüfen | fehlt ein Wert: Enzo fragen, die globale Konfiguration nicht selbst ändern |
| 3 | `.gitignore` passend zur Sprache anlegen | vor dem ersten Commit |
| 4 | `README.md` mit Zweck des Vorhabens anlegen | ein Absatz genügt am Anfang |
| 5 | erster Commit: `chore: initialize repository` | danach beginnt die Arbeit in Branches |

### Ort des Repositorys

- Nennt Enzo einen Ort, wird genau dort angelegt.
- Nennt Enzo keinen Ort, wird einmal gefragt, zusammen mit den übrigen offenen Fragen. Der Ort wird nie geraten.
- Ein Repository gehört nicht in den Obsidian-Vault und nicht in einen mit einer Cloud synchronisierten Ordner (Google Drive, iCloud), weil die Synchronisation das Verzeichnis `.git` beschädigen kann. Nennt Enzo einen solchen Ort, wird einmal darauf hingewiesen und danach seine Entscheidung befolgt.

### Entferntes Repository

- Bei den Größenklassen Mittel und Groß wird einmal gefragt, ob ein entferntes Repository auf GitHub angelegt werden soll.
- Neue entfernte Repositorys sind privat, solange Enzo nichts anderes sagt.
- Mit entferntem Repository wird nach jedem zusammengeführten Arbeitspaket `git push` ausgeführt, damit der Stand gesichert ist.

## Feature-Branch-Workflow

- `main` enthält nur fertige und geprüfte Stände.
- Jede neue Funktionalität, also jedes Arbeitspaket, bekommt einen eigenen Branch, der von `main` abzweigt.
- Branchname: `<typ>/<kurzbeschreibung>`, zum Beispiel `feat/import-groundwater-levels`. Der Typ entspricht den Typen der Commit-Nachrichten.
- Erst nach Fertigstellung und Freigabe durch Enzo wird der Branch in `main` zusammengeführt. Danach wird er gelöscht.
- Größenklasse Klein: Bis zur ersten abgenommenen Fassung darf direkt auf `main` gearbeitet werden. Jede spätere Änderung läuft über einen Branch.

## Commits

Die Historie soll übersichtlich sein und jede Nachricht die Änderung gut beschreiben. Ein Commit enthält genau eine logische Änderung und hinterlässt einen lauffähigen Stand.

### Form: Conventional Commits

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

| Typ | Bedeutung |
|---|---|
| `feat` | neue Funktion |
| `fix` | Fehlerbehebung |
| `refactor` | Umstrukturierung ohne geändertes Verhalten |
| `docs` | Dokumentation |
| `test` | Tests |
| `chore` | Wartung: Abhängigkeiten, Konfiguration, automatische Prüfungen |

Der Scope steht in runden Klammern und nennt den betroffenen Teil, zum Beispiel das Modul.

### Regeln für die Nachricht

1. Betreffzeile und Text durch eine Leerzeile trennen.
2. Betreffzeile höchstens 50 Zeichen.
3. Kein Punkt am Ende der Betreffzeile.
4. Befehlsform in der Betreffzeile. Probe: "If applied, this commit will ...".
5. Text bei 72 Zeichen umbrechen.
6. Der Text erklärt was und warum, nicht wie.
7. Englisch.

### Beispiel

Gut:

```
feat(import): read groundwater levels from csv

Station files from the field loggers use semicolons and a
comma as decimal separator. Parse them explicitly instead of
relying on pandas defaults, which silently produced strings.

Refs #4
```

Schlecht: `something commited` (sagt nichts aus), `Change code` (welcher Code?), `Added bounce model` (keine Befehlsform).

### Vor jedem Commit

- `git status` und `git diff --staged` ansehen.
- Dateien gezielt mit `git add <datei>` vormerken, nicht pauschal alles.
- Die Abschlussprüfung des Sprach-Codex ist bestanden, für Python siehe `python-codex`.
- Nie in ein Repository: Zugangsdaten, Rohdaten, große Binärdateien, virtuelle Umgebungen.

## Arbeitspakete als Issues

Ein Issue ist ein klar abgegrenzter, nachverfolgbarer Arbeitsauftrag. Jedes Arbeitspaket aus dem Projektstrukturplan ist ein Issue.

- Bestandteile: Titel, in dem die Aufgabe steckt, Beschreibung, Labels, Verweis auf den Branch.
- Definition of Done: Der gewünschte Endzustand ist eindeutig. Grundlage ist das Abnahmekriterium des Arbeitspakets.
- Mit entferntem Repository auf GitHub: je Arbeitspaket ein Issue. Der Pull Request verweist mit `Closes #<nummer>` darauf.
- Ohne entferntes Repository: Der Projektstrukturplan in der Entwurfsnotiz ist die Liste der Issues.
- Lebenszyklus: offen, in Arbeit, im Review, geschlossen. Ein abgelehntes Review führt mit Begründung zurück in die Bearbeitung.

## Review vor dem Zusammenführen

Jedes Arbeitspaket wird vor dem Zusammenführen geprüft. Der Assistent ist Autor, Enzo ist Reviewer. Der Autor führt vorher die Selbstprüfung durch:

| Art | Prüffragen |
|---|---|
| Einordnung | Kontext, Risiko, Umfang der Änderung, Stand der Tests |
| Entwurf und Architektur | Schnittstellen, Kopplung, Grenzen der Module, Benennung |
| Sicherheit und Datenschutz | Eingaben geprüft, keine Zugangsdaten, neue Abhängigkeiten begründet |
| Tests | Normalfall, Randfälle, Fehlerpfade |
| Leistung und Betrieb | häufig durchlaufene Stellen, unnötige Wiederholungen, Rückweg bei Fehlschlag |
| Oberfläche | nur bei Bedienoberflächen: Verständlichkeit, Fehlermeldungen, Bedienbarkeit |

Danach wird die Freigabe angefragt mit: was sich geändert hat, warum, Stand der Tests, bekannte Lücken.

- Mit entferntem Repository: als Pull Request.
- Ohne entferntes Repository: als Zusammenfassung im Chat mit der Ausgabe von `git diff main...<branch> --stat`.

Zusammengeführt wird erst nach ausdrücklicher Freigabe durch Enzo.

## Rückgängig machen

- Bereits geteilte Commits werden mit `git revert` zurückgenommen. Ihre Historie wird nicht umgeschrieben.
- `git reset --hard`, `git push --force` und das Löschen eines Branches mit nicht zusammengeführten Commits erfolgen nur nach ausdrücklicher Zustimmung.
- Nicht committete Änderungen, die nicht vom Assistenten stammen, werden nie verworfen, sondern zuerst gemeldet.

## Meilensteine und Nachvollziehbarkeit

- Jede abgenommene Fassung bekommt ein Tag, beginnend mit `v0.1.0`.
- Arbeit des Assistenten wird dokumentiert und kritisch geprüft: Das Umsetzungsprotokoll nennt je Arbeitspaket Branch, Commit und was Enzo geprüft hat.

## Herkunft der Regeln

| Herkunft | Regeln |
|---|---|
| Einheit "Git" | Feature-Branch-Workflow, Regeln für Commit-Nachrichten, Conventional Commits mit Typen und Scope |
| Einheit "Projektplanung" | Issues, Definition of Done, Pull Request, Arten des Code-Reviews, Lebenszyklus |
| Übungsdokument | Fortschritt in Git nachvollziehbar, Arbeit künstlicher Intelligenz dokumentieren und prüfen |
| Ergänzung für Einzelvorhaben | Ort des Repositorys, `.gitignore`, Branchnamen, Tags, Schutz vor zerstörenden Befehlen, Ausnahme für die Größenklasse Klein |