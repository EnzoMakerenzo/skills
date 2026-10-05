---
name: "projekt-codex"
description: "Vorgehen für Programmiervorhaben: zuerst Konzept nach Projekt Management Austria, dann Entwurf, Umsetzung, Abnahme. Verwenden, sobald ein neues Skript, Werkzeug oder Softwareprojekt begonnen, wesentlich erweitert oder ein bestehendes übernommen wird. Nicht verwenden bei reinen Fragen und Erklärungen, bei denen kein Code entsteht. Vorrang: greift zuerst, vor git-codex und dem Codex der Sprache."
---

# Projekt-Codex: Vorgehen bei Programmiervorhaben

## Zweck

Code, der ohne geklärtes Ziel entsteht, löst oft das falsche Problem sauber. Dieser Codex legt deshalb fest, dass vor dem ersten Code ein freigegebenes Konzept steht. Die Begriffe folgen den Methoden des Projektstartprozesses von Projekt Management Austria, verkleinert auf Softwarevorhaben einer Einzelperson.

## Grundregel: Phasensperre

Jede Phase endet mit einem Ergebnis, das Enzo ausdrücklich freigibt. Vor der Freigabe beginnt die nächste Phase nicht. Schweigen ist keine Freigabe. Offene Fragen werden gesammelt in einer Nachricht gestellt, nicht einzeln.

Sagt Enzo ausdrücklich "direkt umsetzen", genügt ein Kurzkonzept in fünf Zeilen als erste Antwort, danach folgt sofort die Umsetzung.

## Ablage in Obsidian

Alle Projektdokumente (Konzept, Entwurf, Umsetzungsprotokoll, Abnahmebericht, Abschluss) werden als Markdown-Notizen in Obsidian abgelegt. Der Chat ist nur der Ort für Abstimmung und Freigabe, nicht das Archiv: Was nur im Chat steht, ist beim nächsten Vorhaben nicht mehr auffindbar.

### Ablageort klären

- Nennt Enzo Vault und Ordner, wird genau dort abgelegt.
- Nennt Enzo keinen Ablageort, wird einmal gefragt, bevor die erste Notiz geschrieben wird: welcher Vault und welcher Ordner darin. Die Frage steht in derselben Nachricht wie die übrigen offenen Fragen der Konzeption.
- Der Ablageort wird nie geraten und nie aus einem früheren Vorhaben übernommen. Es wird auch kein neuer Ordner auf oberster Ebene des Vaults angelegt, ohne dass Enzo ihn genannt hat.
- Ein einmal genannter Ablageort gilt für das gesamte Vorhaben.
- Ist der Vault in der Sitzung nicht erreichbar, wird der Zugriff auf den Ordner angefragt. Gelingt das nicht, wird das Dokument im Chat geliefert und in der ersten Zeile gesagt, dass es nicht abgelegt wurde. Ein anderer Speicherort wird nicht stillschweigend ersetzt.

### Aufbau im Vault

Bestehende Konventionen des Vaults haben Vorrang: Vor dem Anlegen wird die vorhandene Struktur angesehen (Ordner, Benennung, Eigenschaften, Vorlagen) und übernommen. Gibt es keine, gilt dieser Aufbau:

| Notiz | Inhalt | Entsteht in |
|---|---|---|
| `<Projektname>.md` | Übersicht: Stand, Verweise auf alle Notizen, Ort des Repositorys | Phase 1 |
| `01 Konzept.md` | Ergebnis der Konzeption | Phase 1 |
| `02 Entwurf.md` | Objektstrukturplan, Projektstrukturplan, Meilensteine | Phase 2 |
| `03 Umsetzungsprotokoll.md` | je Arbeitspaket: Ergebnis, Branch, Commit, Abweichungen, Entscheidungen mit Datum | Phase 3 |
| `04 Abnahme.md` | Prüfergebnis je Abnahmekriterium | Phase 4 |
| `05 Abschluss.md` | Bedienungsanleitung, offene Punkte, Erkenntnisse | Phase 5 |

Alle Notizen liegen in einem eigenen Ordner `<Projektname>/` unter dem genannten Ablageort. Bei der Größenklasse Klein genügt eine einzige Notiz `<Projektname>.md` mit Kurzkonzept, Ergebnis und Ort des Repositorys.

### Regeln für die Notizen

- Jede Notiz beginnt mit Eigenschaften: `typ`, `projekt`, `phase`, `status`, `erstellt`.
- `status` ist `entwurf`, bis Enzo die Phase freigibt. Erst nach ausdrücklicher Freigabe wird `status: freigegeben` und `freigegeben_am` gesetzt. So zeigt der Vault den Stand der Phasensperre.
- Notizen verweisen mit Wikilinks aufeinander, die Übersichtsnotiz verweist auf alle.
- Vorhandene Notizen werden nie überschrieben. Änderungen nach einer Freigabe kommen als datierter Abschnitt hinzu, damit nachvollziehbar bleibt, was freigegeben war.
- Code liegt nicht im Vault, sondern in seinem eigenen Git-Repository. Die Übersichtsnotiz nennt dessen Pfad. Nur wenn Enzo es ausdrücklich verlangt, wird Code im Vault abgelegt.

## Versionsverwaltung mit Git

Für jedes Vorhaben wird ein Git-Repository angelegt, auch bei der Größenklasse Klein. Kein Code entsteht außerhalb eines Repositorys. Die Einzelheiten regelt der Skill `git-codex`: Anlegen des Repositorys, Feature-Branch-Workflow, Commit-Nachrichten, Issues und Review.

| Begriff im Projekt-Codex | Entsprechung in Git |
|---|---|
| Arbeitspaket | ein Issue und ein eigener Branch |
| Abnahmekriterium des Arbeitspakets | Definition of Done des Issues |
| Freigabe durch Enzo | Voraussetzung für das Zusammenführen in `main` |
| Abgenommene Fassung | Tag auf `main` |

- Nennt Enzo keinen Ort für das Repository, wird einmal danach gefragt, in derselben Nachricht wie nach dem Ablageort in Obsidian.
- Das Repository entsteht nach der Freigabe des Entwurfs und vor der ersten Zeile Code, bei der Größenklasse Klein nach der Freigabe des Kurzkonzepts.

## Codequalität je Sprache

Für jede Programmiersprache des Vorhabens gilt ein eigener Codex, für Python `python-codex`. Der Skill `sprach-codex` klärt vor dem ersten Code in einer Sprache, ob ein Codex vorhanden ist, und entwirft einen fehlenden. Die Sprachen und ihre Codizes stehen im Entwurf.

## Größenklasse zuerst bestimmen

| Klasse | Merkmal | Umfang der Konzeption |
|---|---|---|
| Klein | eine Datei, bis etwa 100 Zeilen, einmaliger Zweck | Kurzkonzept: Ziel, Nicht-Ziele, Eingaben, Ausgaben, Abnahmekriterien |
| Mittel | mehrere Module oder wiederkehrende Nutzung | vollständige Phasen 1 und 2, je eine Notiz |
| Groß | mehrere Wochen, externe Nutzer oder Daten Dritter | vollständige Phasen 1 und 2, Risiken und Umwelten ausführlich |

Die gewählte Klasse wird in der ersten Zeile des Konzepts genannt, damit Enzo sie korrigieren kann.

## Bestehende Vorhaben: Bestandsübernahme

Gibt es zu einem Vorhaben schon Code oder Unterlagen, ersetzt die Bestandsübernahme den Einstieg über Phase 1 und 2. Grundsatz: erst sichern, dann verstehen, dann ändern. Bis zur Sicherung in Schritt 2 wird nichts verändert, und bis zur Freigabe des nachträglichen Konzepts gibt es keine inhaltliche Änderung am Code.

| Schritt | Handlung | Ergebnis |
|---|---|---|
| 1 Bestandsaufnahme | nur lesen: Ordner, Sprachen, Abhängigkeiten, vorhandenes Repository, Unterlagen, lauffähig oder nicht | Übersichtsnotiz mit Stand, Lücken und Risiken |
| 2 Sicherung | Ist-Stand unverändert in Git festhalten, siehe unten | rückholbarer Ausgangsstand mit Tag `baseline` |
| 3 Nachträgliches Konzept | Ziele, Nicht-Ziele und Abnahmekriterien aus dem Bestand ableiten, Erfülltes und Offenes trennen | `01 Konzept.md`, Freigabe durch Enzo |
| 4 Restplanung | nur die offene Arbeit in Arbeitspakete zerlegen, Altlasten als eigene Arbeitspakete | `02 Entwurf.md`, Freigabe durch Enzo |
| 5 Weiterarbeit | normaler Ablauf ab Phase 3 | Arbeitspakete in Branches |

### Sicherung des Ist-Stands

- Ohne Repository: nach `git-codex` anlegen, `.gitignore` ergänzen, ein einziger Commit `chore: import existing state` mit dem unveränderten Stand.
- Mit Repository: Historie und Konventionen bleiben erhalten. Die Regeln des `git-codex` gelten ab dem nächsten Commit.
- Vor dem Commit wird der Bestand auf Zugangsdaten und große Binärdateien geprüft, zum Beispiel 3D-Druckdateien, Konstruktionsdaten und Messdaten. Zugangsdaten werden nicht committet, sondern gemeldet. Bei großen Binärdateien entscheidet Enzo: Git Large File Storage, ein Ordner außerhalb des Repositorys oder Ausschluss.
- Liegt der Ordner in einem mit einer Cloud synchronisierten Verzeichnis, wird nach `git-codex` darauf hingewiesen. Verschoben wird nur auf Enzos Anweisung.

### Regeln für die Weiterarbeit am Bestand

- Kein Großumbau: Der Codex der Sprache gilt für neuen und für angefassten Code. Bestehende Verstöße werden nicht nebenbei bereinigt, sondern als Arbeitspaket erfasst.
- Vor einer Änderung an ungetestetem Code entsteht zuerst ein Test, der das bisherige Verhalten festhält.
- Ein Formatierer läuft erstmals in einem eigenen Commit über den Bestand, getrennt von inhaltlichen Änderungen und erst nach Freigabe, damit spätere Änderungen lesbar bleiben.
- Vermutungen über die Absicht des vorhandenen Codes werden als Annahmen gekennzeichnet.

## Phase 1: Konzeption

Ergebnis ist ein Konzept mit diesen Abschnitten:

1. **Projektauftrag**: Ausgangslage, Problem, wer das Ergebnis nutzt.
2. **Ziele**: Hauptziele, Zusatzziele und ausdrücklich Nicht-Ziele. Nicht-Ziele verhindern, dass der Umfang während der Umsetzung wächst.
3. **Abgrenzung und Kontext**: sachlich (was gehört dazu, was nicht), zeitlich (was war vorher, was kommt danach), sozial (wer ist beteiligt oder betroffen).
4. **Umwelten**: angrenzende Systeme, Datenquellen, Formate, Personen, die den Code später warten.
5. **Abnahmekriterien**: prüfbare Aussagen, zum Beispiel "liest alle Dateien im Ordner und meldet jede übersprungene Datei mit Grund".
6. **Risiken**: die drei wichtigsten mit je einer Gegenmaßnahme.
7. **Offene Fragen**: alles, was Enzo entscheiden muss, einschließlich des Ablageorts in Obsidian und des Orts des Repositorys, falls sie nicht genannt wurden.

Annahmen werden als Annahmen gekennzeichnet, nicht als Tatsachen formuliert.

## Phase 2: Entwurf

1. **Objektstrukturplan**: Module, Datenmodelle, Schnittstellen und wie sie zusammenhängen.
2. **Projektstrukturplan**: Arbeitspakete, jedes mit Ergebnis und eigenem Abnahmekriterium. Ein Arbeitspaket ist klein genug, um es in einem Schritt umzusetzen und zu prüfen.
3. **Meilensteine**: Reihenfolge der Arbeitspakete und der Punkt, an dem erstmals etwas lauffähig ist.
4. **Werkzeuge und Abhängigkeiten**: Sprachen mit zugehörigem Codex, Bibliotheken mit Begründung, Ort des Repositorys, entferntes Repository ja oder nein.

Bei mindestens zwei tragfähigen Lösungswegen werden diese in einer Tabelle gegenübergestellt und einer empfohlen.

## Phase 3: Umsetzung

- Zuerst das Repository nach `git-codex` anlegen.
- Vor dem ersten Code in einer Sprache nach `sprach-codex` klären, welcher Codex gilt.
- Ein Arbeitspaket nach dem anderen, jedes in einem eigenen Branch, jedes endet mit bestandenen Tests.
- Vor dem Zusammenführen in `main`: Selbstprüfung nach `git-codex`, dann Freigabe durch Enzo.
- Nach jedem Arbeitspaket ein Eintrag im Umsetzungsprotokoll mit Branch und Commit.
- Keine Erweiterung des Umfangs ohne Rückfrage. Naheliegende Zusatzideen werden als Vorschlag notiert, nicht eingebaut.
- Weicht die Umsetzung vom Entwurf ab, wird das mit Grund gemeldet, bevor weitergearbeitet wird.

## Phase 4: Abnahme

- Jedes Abnahmekriterium aus Phase 1 einzeln prüfen und das Ergebnis berichten.
- Klar trennen: geprüft und bestanden, geprüft und fehlgeschlagen, nicht prüfbar mit Grund.
- Fehlgeschlagene oder übersprungene Prüfungen stehen an erster Stelle des Berichts, nicht am Ende.
- Nach der Abnahme durch Enzo bekommt der Stand auf `main` ein Tag.

## Phase 5: Abschluss

- Kurze Bedienungsanleitung: Zweck, Installation, Aufruf mit Beispiel. Sie steht als `README.md` im Repository und als Notiz in Obsidian.
- Offene Punkte und bekannte Grenzen.
- Erkenntnisse, die beim nächsten Vorhaben helfen, in zwei bis drei Sätzen. Dazu gehören Änderungsvorschläge für einen Codex, dessen Regel gefehlt oder nicht getragen hat.
- Übersichtsnotiz auf den Endstand bringen: Status, Verweise, Ort des Repositorys, letztes Tag.

## Vorlage Kurzkonzept

```
Größenklasse: Klein
Ziel: <ein Satz>
Nicht-Ziele: <was bewusst fehlt>
Eingaben und Ausgaben: <Formate, Orte>
Abnahmekriterien: <zwei bis vier prüfbare Aussagen>
Ablageort in Obsidian: <Vault und Ordner, oder Frage an Enzo>
Ort des Repositorys: <Pfad, oder Frage an Enzo>
Offene Fragen: <oder "keine">
```