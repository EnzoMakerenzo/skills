---
name: "chat-analyse"
description: "Wertet den gesamten Chatverlauf aus einem claude.ai-Datenexport aus und schlägt Skills vor: zählt exakt, welche Skills und Werkzeuge genutzt wurden, erkennt wiederkehrende Aufgabenmuster und empfiehlt je Muster, einen vorhandenen Skill zu nutzen, zu erweitern oder einen neuen anzulegen. Verwenden, wenn Enzo seinen Chatverlauf, einen Export mit conversations.json oder seine Skill-Nutzung auswerten will oder fragt, welche Skills er braucht. Nicht verwenden zum Anlegen oder Ändern eines Skills, dafür gilt skill-creator, und nicht für die automatische Auswahl von Skills während der Arbeit."
---

# Chat-Analyse: Skill-Vorschläge aus dem Chatverlauf

## Zweck

Welche Skills sich lohnen, zeigt der eigene Chatverlauf: Aufgaben, die immer wieder ohne passenden Skill erledigt werden, sind Kandidaten für einen neuen Skill; Skills, die selten geladen werden, obwohl ihre Aufgaben oft vorkommen, werden zu wenig genutzt. Dieser Skill liefert dazu einen Bericht mit exakten Zählungen und begründeten Vorschlägen, über die Enzo entscheidet.

## Grundregeln

- Zählungen kommen nur aus dem Skript. Zahlen werden nie geschätzt oder aus dem Gedächtnis ergänzt.
- Vorschläge sind Vorschläge: Kein Skill wird angelegt, geändert, installiert oder deaktiviert. Enzo gibt jeden Vorschlag einzeln frei.
- Der Export und alle Zwischendateien enthalten persönliche Chatinhalte. Sie liegen nie in einem Git-Repository; das Skript verweigert einen Ausgabeordner in einem Repository.
- Der Bericht enthält Zählungen, Muster, Vorschläge und Chat-Kennungen, aber keine Zitate, keine Chattitel und keine Zusammenfassungen aus Chats.
- Ein Vorschlag erscheint erst ab drei Chats mit demselben Muster.
- Was nicht prüfbar war, steht im Bericht als nicht prüfbar, mit Grund.

## Voraussetzungen

| Was | Woher |
|---|---|
| `conversations.json` | Datenexport in den claude.ai-Einstellungen anfordern; der Link kommt per E-Mail; die Datei steckt in `conversations-000.zip`. Die Links gelten 24 Stunden und oft nur für einen Abruf. |
| Python ab 3.10 | nur Standardbibliothek, keine Installation nötig |
| Code | Ordner `chat-analyse/src` im Repository `EnzoMakerenzo/skills`; fehlt er, wird er nach Schritt 0 geladen |
| Ablageort des Berichts | von Enzo genannt; ohne Angabe einmal fragen |

Projektzuordnung, Cowork-Sitzungen und Design-Chats stehen in anderen Dateien des Exports und sind nicht Teil der Auswertung.

## Ablauf

### 0 Code bereitstellen

Die im Konto gespeicherte Fassung dieses Skills enthält nur diese Datei, nicht das Skript. Deshalb zuerst den Code suchen, in dieser Reihenfolge:

1. Neben dieser `SKILL.md` liegt ein Ordner `src/chat_analyse`: diesen nutzen.
2. Ein verbundener Ordner enthält das Repository `skills` mit `chat-analyse/src/chat_analyse`: diesen nutzen.
3. Sonst den Code aus dem öffentlichen Repository laden, in einen eigenen, leeren Ordner außerhalb jedes Git-Repositorys, zum Beispiel im Arbeits- oder Notizordner der Sitzung:

```
mkdir -p <arbeitsordner>/chat-analyse-code
curl -sSL https://codeload.github.com/EnzoMakerenzo/skills/tar.gz/refs/heads/main \
  | tar xz -C <arbeitsordner>/chat-analyse-code
```

Der Code liegt danach in `<arbeitsordner>/chat-analyse-code/skills-main/chat-analyse/src`. Gelingt der Abruf nicht (kein Netz, Adresse gesperrt), wird abgebrochen und gemeldet, welcher Abruf scheiterte; Zählungen werden nie ohne das Skript erstellt. Im Bericht steht, welcher der drei Wege genutzt wurde.

### 1 Skript ausführen

```
PYTHONPATH=<code-ordner>/src python3 -m chat_analyse <pfad>/conversations.json
```

`<code-ordner>` ist der Ordner `chat-analyse` aus Schritt 0. Liegt der Export in einem Git-Repository, wird `--output-dir` auf einen Ordner außerhalb gesetzt; das Skript verweigert sonst die Ausgabe.

Ohne `--output-dir` schreibt das Skript in den Ordner `auswertung` neben dem Export:

| Datei | Inhalt |
|---|---|
| `zaehlung.json` | Chats, Zeitraum, Skill-Aufrufe, gelesene `SKILL.md`, Nutzungen und Chats je Skill, Werkzeuge, Nutzungen je Monat, übersprungene Chats mit Grund |
| `merkmale.jsonl` | je Chat eine Zeile: Kennung, Datum, Titel, Zusammenfassung (gekürzt auf 400 Zeichen), erste Anfrage nur bei fehlender Zusammenfassung, Werkzeuge, Skills |

Der Prüfbericht des Skripts wird unverändert in den Bericht übernommen. Endet das Skript mit Fehler, wird abgebrochen und der Fehler gemeldet.

Zählregel: Ein Skill gilt als genutzt bei einem Aufruf über das Werkzeug `Skill` oder beim Lesen seiner installierten `SKILL.md` (unter `/mnt/skills/` oder `.claude/skills/`). Eine `SKILL.md` in einem Arbeitsordner oder Repository wird bearbeitet, nicht genutzt. Präfixe wie `anthropic-skills:` werden entfernt.

### 2 Installierte Skills erfassen

Grundlage ist die Liste der Skills, die in der laufenden Sitzung verfügbar sind, mit Name und Beschreibung. Liegt eine Übersicht wie `TechStack/Skill-Index.md` vor, wird sie ergänzend gelesen. Skills, die im Export vorkommen, aber nicht mehr installiert sind, werden als solche gekennzeichnet.

### 3 Muster bilden

- `merkmale.jsonl` vollständig lesen. Passt die Datei nicht in einen Durchgang, wird in Blöcken nach Monaten gelesen und die Muster danach zusammengeführt.
- Ein Muster ist eine wiederkehrende Aufgabe, benannt als Tätigkeit mit Gegenstand, zum Beispiel „Mac per AppleScript bedienen" oder „Word-Dokument erstellen", nicht ein Thema wie „Landwirtschaft".
- Jeder Chat bekommt genau ein Hauptmuster. Chats ohne erkennbare Aufgabe (Plauderei, Testnachricht) gehen in „ohne Aufgabe".
- Werkzeuge stützen die Zuordnung: Ein Chat mit vielen Aufrufen von `osascript` gehört eher zu Mac-Bedienung als zu Recherche.
- Je Muster werden die Kennungen der Chats festgehalten, damit jede Zuordnung nachprüfbar ist.

### 4 Abgleich und Vorschläge

Für jedes Muster mit mindestens drei Chats:

| Art | Bedingung | Inhalt des Vorschlags |
|---|---|---|
| nutzen | ein installierter Skill deckt die Aufgabe ab, wurde in diesen Chats aber selten geladen | welcher Skill, in wie vielen Chats des Musters er geladen wurde, wie die Beschreibung den Auslöser verfehlt |
| erweitern | ein installierter Skill deckt einen Teil ab | welcher Skill, welcher Teil fehlt |
| neu | kein installierter Skill passt | vorgeschlagener Name, Zweck in einem Satz, nächstliegender geprüfter Skill und warum er nicht passt |

- „neu" nur, wenn die Beschreibungen aller installierten Skills geprüft sind und keine passt; der nächstliegende geprüfte Skill wird genannt.
- Muster, die ein Skill schon gut abdeckt (Skill in mindestens der Hälfte der Chats des Musters geladen), werden ohne Vorschlag aufgeführt.
- Reihenfolge der Vorschläge: nach Anzahl Chats im Muster, absteigend.

### 5 Stichprobe

Zehn Chat-Kennungen aus den drei größten Mustern, verteilt über die Muster, mit zugeordnetem Muster. Enzo prüft die Zuordnung. Weicht sie bei mehr als zwei Chats ab, werden die Muster überarbeitet, bevor Vorschläge freigegeben werden.

### 6 Bericht schreiben

Bericht nach der Vorlage unten am genannten Ablageort, Dateiname `JJJJ-MM-TT Bericht.md`. Ein vorhandener Bericht wird nicht überschrieben.

### 7 Abschlussprüfung

Vor der Übergabe einzeln prüfen und im Bericht festhalten:

1. Anzahl Chats, Zeitraum und jeder übersprungene Chat mit Grund stehen im Bericht.
2. Jeder Vorschlag nennt Muster, Anzahl Chats und Art.
3. Kein Vorschlag stützt sich auf weniger als drei Chats.
4. Jeder Vorschlag „neu" nennt den nächstliegenden geprüften Skill.
5. Der Bericht enthält keine Zitate, Titel oder Zusammenfassungen aus Chats.
6. Kein Export und keine Zwischendatei liegt in einem Git-Repository.

## Vorlage Bericht

```
---
typ: bericht
projekt: Chat-Analyse
erstellt: <JJJJ-MM-TT>
status: entwurf
---

# Skill-Analyse <JJJJ-MM-TT>

## Datengrundlage
<Prüfbericht des Skripts: Chats, Zeitraum, übersprungene Chats, Skill-Aufrufe, gelesene SKILL.md, Chats mit Skill-Nutzung>
<Weg zum Code aus Schritt 0 und Stand (Commit oder Download von main mit Datum)>

## Skill-Nutzung
| Skill | Nutzungen | Chats | installiert |

## Muster
| Muster | Chats | geladene Skills | Vorschlag |

## Vorschläge
| Nr. | Muster | Art | Skill | Begründung |

## Stichprobe
| Chat-Kennung | Muster | Prüfung durch Enzo |

## Abschlussprüfung
| Nr. | Prüfung | Ergebnis |

## Grenzen
<nicht ausgewertete Teile des Exports, nicht prüfbare Punkte>
```

## Arbeiten mit lokalen Modellen

Das Skript braucht nur Python. Bei kleinem Kontextfenster, etwa unter pi auf dem GX10, wird `merkmale.jsonl` in Monatsblöcken gelesen; je Block entstehen Muster mit Chat-Kennungen, die am Ende zusammengeführt werden. Die Zählungen bleiben exakt, weil sie aus `zaehlung.json` stammen.

## Herkunft der Regeln

| Herkunft | Regeln |
|---|---|
| Vorhaben Chat-Analyse, Konzept und Entwurf vom 2026-10-29 | Ziel, Abnahmekriterien, Lösungsweg „Python zählt, Claude bildet Muster" |
| Prüfung des echten Exports | Aufbau von `conversations.json`, Zählregel für installierte `SKILL.md` |
| `projekt-codex` | Freigabe durch Enzo, Kennzeichnung nicht prüfbarer Punkte |
