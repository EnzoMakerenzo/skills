---
name: "matlab-codex"
description: "Regeln für sauberen MATLAB-Code mit Grenzwerten, Werkzeugen (Code Analyzer, matlab.unittest, Build Tool) und Abschlussprüfung. Verwenden bei jedem Schreiben, Ändern oder Prüfen von MATLAB-Code. Nicht verwenden bei reinen Rechenfragen, bei denen kein Code entsteht. Vorrang: gilt nach projekt-codex und zusätzlich zu git-codex."
---

# MATLAB-Codex: Regeln für sauberen Code

## Zweck

Berechnungen in MATLAB entstehen oft als schnelles Skript und werden dann weitergereicht. Die Regeln zielen darauf, dass Enzo oder eine Kollegin eine Berechnung in einem Jahr ohne Rückfrage versteht, erneut ausführt und dasselbe Ergebnis erhält. Grenzwerte sind Richtwerte: Eine Abweichung ist erlaubt, wenn sie in einer Zeile begründet wird.

Vorhandene Konventionen eines bestehenden Projekts haben Vorrang vor diesem Codex. Für das Vorgehen vor dem ersten Code gilt `projekt-codex`, für die Versionsverwaltung `git-codex`.

## Werkzeuge

| Aufgabe | Werkzeug | Aufruf |
|---|---|---|
| Formatierung | Editor, automatische Einrückung | im Editor, kein Aufruf in der Abschlussprüfung |
| Statische Prüfung | Code Analyzer | `codeIssues("src")` |
| Tests | matlab.unittest | `runtests("tests")` |
| Beides in einem Schritt | Build Tool | `buildtool check test` |
| Von der Befehlszeile | MATLAB ohne Oberfläche | `matlab -batch "buildtool check test"` |

MATLAB hat keine statische Typprüfung. Ihren Platz nimmt der `arguments`-Block am Anfang jeder Funktion ein, siehe Abschnitt Typen.

Was ein Werkzeug erzwingt, wird nicht von Hand diskutiert. Grundkonfiguration `buildfile.m` im Projektordner:

```matlab
function plan = buildfile
import matlab.buildtool.tasks.CodeIssuesTask
import matlab.buildtool.tasks.TestTask

plan = buildplan(localfunctions);
plan("check") = CodeIssuesTask;
plan("test") = TestTask;
plan.DefaultTasks = ["check" "test"];
end
```

Das Build Tool und seine Aufgabenklassen setzen eine aktuelle MATLAB-Version voraus. Fehlen sie in der installierten Version, werden `codeIssues` und `runtests` einzeln aufgerufen, und das wird in der Übergabe gesagt. Die Grenzwerte für Anweisungen, Parameter und Verschachtelung prüft der Code Analyzer nicht, sie werden beim Review geprüft.

## Benennung

- Namen sagen, was der Wert bedeutet, nicht welchen Typ er hat: `groundwaterLevelM` statt `data2`.
- Variablen und Funktionen in `lowerCamelCase`, Klassen, Eigenschaften und Namen-Wert-Argumente in `UpperCamelCase`, Namensräume kurz und kleingeschrieben.
- Höchstens 32 Zeichen je Name.
- Ausgeschriebene Wörter. Ausnahmen: Laufvariablen in Schleifen bis drei Zeilen und Formelzeichen innerhalb einer mathematischen Formel, die im Kommentar mit Quelle benannt ist.
- Physikalische Größen tragen die Einheit im Namen: `depthCm`, `conductivityUsPerCm`, `durationS`. In Tabellen zusätzlich `VariableUnits` setzen.
- Funktionen heißen nach dem, was sie tun, Umwandlungen mit `2` (`depthsCm2M` ist erlaubt, `depthsToMeters` ist besser lesbar). Wahrheitswerte beginnen mit `is` oder `has`, ohne Verneinung im Namen.
- Bezeichner auf Englisch, Kommentare und Hilfetexte auf Deutsch.
- Keine Namen, die vorhandene MATLAB-Funktionen überdecken: `sum`, `max`, `table`, `i`, `j`. Prüfen mit `which <name>`.

## Funktionen

- Eine Funktion erledigt eine Aufgabe. Braucht die Beschreibung ein "und", wird geteilt.
- Richtwerte: höchstens 30 Anweisungen, höchstens 4 Eingabeparameter, höchstens 4 Rückgabewerte, Verschachtelung höchstens 3 Ebenen. Das ist strenger als die Vorgabe von MathWorks (6 Eingaben, 5 Ebenen), damit alle Sprachen gleich streng sind.
- Mehr als 4 zusammengehörige Parameter werden zu Namen-Wert-Argumenten im `arguments`-Block oder zu einer Struktur.
- Keine booleschen Schalterparameter, die das Verhalten umschalten. Stattdessen zwei Funktionen.
- Kein `varargin` und kein `nargin`-Verzweigen. Optionale Werte stehen als Namen-Wert-Argumente mit Standardwert im `arguments`-Block.
- Frühe Rückgabe statt tiefer Verschachtelung.
- Berechnung und Ein-/Ausgabe trennen: Funktionen, die rechnen, lesen keine Dateien, schreiben keine und öffnen keine Abbildungen.
- Funktionen statt Skripte. Ein Skript ist nur Einstiegspunkt und ruft Funktionen auf.

## Struktur

| Ordner oder Datei | Inhalt |
|---|---|
| `src/` | Funktionen und Klassen, eine öffentliche Funktion je Datei, Dateiname gleich Funktionsname |
| `src/+<name>/` | Namensraum für zusammengehörige Funktionen |
| `scripts/` | Einstiegsskripte, nummeriert nach Ablauf |
| `tests/` | Testklassen |
| `data/raw/`, `data/processed/` | Rohdaten nur lesen, abgeleitete Daten getrennt |
| `buildfile.m` | Prüf- und Testaufgaben |

- Dateien bis etwa 300 Zeilen. Hilfsfunktionen, die nur eine Datei braucht, stehen als lokale Funktionen an deren Ende.
- Der Suchpfad wird an einer Stelle gesetzt, in einem MATLAB-Projekt oder in einem einzigen Startskript. Kein `addpath` und kein `cd` verstreut im Code.
- Kein `clear all`, `close all` oder `clc` in Funktionen.
- Kein `global`, kein `eval`, `evalin` oder `assignin`. Werte werden als Argumente übergeben.
- Keine magischen Zahlen: benannte Konstanten mit Einheit, als lokale Variable oder als `properties (Constant)` einer Klasse.
- Pfade mit `fullfile` und `fileparts`, nie als zusammengesetzte Zeichenketten.

## Typen

- Jede öffentliche Funktion beginnt mit einem `arguments`-Block, der Größe, Klasse und Wertebereich festlegt: `depthsCm (1,:) double {mustBeNonnegative}`.
- Text als Zeichenkettenfeld in doppelten Anführungszeichen, nicht als Zeichenvektor in einfachen, außer eine Schnittstelle verlangt es.
- Tabellen (`table`, `timetable`) statt paralleler Felder oder Zellfelder für Messreihen.
- Fehlende Werte sind `NaN`, `NaT` oder `missing` und werden an genau einer Stelle mit `ismissing` behandelt.
- Daten an Systemgrenzen beim Einlesen prüfen: `detectImportOptions`, dann Spaltentypen ausdrücklich setzen.

## Fehlerbehandlung

- Fehler mit Kennung und Meldung auslösen: `error("<projekt>:<funktion>:<grund>", "...", wert)`. Die Meldung nennt den erhaltenen Wert und die Erwartung.
- Jeder `try`-Block hat einen `catch`-Block. Dieser prüft `exception.identifier`, behandelt nur bekannte Fehler und löst Unbekanntes mit `rethrow` erneut aus.
- `try` und `catch` nicht für den normalen Ablauf verwenden.
- Fehler und Warnungen nie stillschweigend schlucken. `warning("off", ...)` nur mit Kennung, Kommentar und Rücksetzen über `onCleanup`.
- Geöffnete Dateien und geänderte Zustände über `onCleanup` zurücksetzen.
- Übersprungene Datensätze werden gezählt und gemeldet.

## Besonderheiten

- Jede Anweisung endet mit Strichpunkt. Ausgaben entstehen ausdrücklich mit `disp` oder `fprintf`.
- Eine Anweisung je Zeile, Einrückung 4 Leerzeichen, Zeilen bis 120 Zeichen.
- Vektorisieren, wo es die Lesbarkeit erhält. Eine klare Schleife ist besser als ein undurchsichtiger Einzeiler.
- Felder vor Schleifen in voller Größe anlegen.
- Gleitkommazahlen nie mit `==` oder `~=` vergleichen, sondern mit Toleranz: `abs(a - b) < tolerance` oder `ismembertol`.
- Der Laufindex einer `for`-Schleife wird im Rumpf nicht verändert.
- Indizes beginnen bei 1. Bei Daten aus anderen Systemen wird die Umrechnung an genau einer Stelle gemacht und kommentiert.
- Zeitangaben als `datetime` mit ausdrücklich gesetzter `TimeZone`.
- Dezimaltrennzeichen und Spaltentrenner beim Einlesen ausdrücklich angeben. Dateien aus österreichischen Systemen haben oft Strichpunkt und Dezimalkomma: `DecimalSeparator=","`, `Delimiter=";"`.
- Zufallszahlen mit `rng(<startwert>)`.
- Rohdaten werden nie überschrieben. Ergebnisse gehen in eigene Dateien.

## Tests

- Jedes Arbeitspaket bringt seine Tests mit.
- Getestet wird Verhalten, nicht die innere Umsetzung.
- Tests sind Klassen, die von `matlab.unittest.TestCase` erben. Datei und Klasse heißen `<Gegenstand>Test.m`, Methoden nennen Bedingung und Erwartung.
- Pflichtfälle: Normalfall, leere Eingabe, `NaN`, Grenzwerte, ungültige Eingabe.
- Zahlen mit `verifyEqual(..., AbsTol=...)` vergleichen, Fehler mit `verifyError` und der erwarteten Kennung.
- Kein Netzwerk und keine echten Produktivdaten in Tests. Kleine Beispieldateien unter `tests/data/`.

## Kommentare und Dokumentation

- Kommentare erklären das Warum, nicht das Was. Sie stehen vor dem Code, den sie erklären, mit einem Leerzeichen nach `%`.
- Jede Funktion hat direkt nach der Kopfzeile eine H1-Zeile und einen Hilfetext mit Aufruf, Eingaben mit Einheit und Ausgaben.
- Formeln aus der Literatur tragen die Quelle im Kommentar.
- `%%` gliedert Skripte in Abschnitte.
- Kein auskommentierter Code, keine Notiz ohne Kontext.

## Abhängigkeiten

- Basis-MATLAB zuerst. Jede Toolbox wird mit einem Satz begründet, weil sie eine eigene Lizenz voraussetzt.
- Benötigte Toolboxen ermitteln mit `matlab.codetools.requiredFilesAndProducts` und in der `README.md` nennen, zusammen mit der MATLAB-Version, mit der geprüft wurde.
- Die MATLAB-Version wird aus dem Projekt übernommen.

## Beispiel

Schlecht:

```matlab
function r = proc(d, f)
r = [];
for i = 1:length(d)
    if d(i) > 0
        if f, r(end+1) = d(i) * 0.01; else, r(end+1) = d(i); end
    end
end
```

Gut:

```matlab
function depthsM = depthsToMeters(depthsCm)
%DEPTHSTOMETERS Rechnet Abstichmaße von Zentimeter in Meter um.
%   depthsM = depthsToMeters(depthsCm) gibt die Abstichmaße in Meter in
%   gleicher Reihenfolge zurück. depthsCm ist ein Zeilenvektor in
%   Zentimeter. Negative Werte lösen einen Fehler aus.
arguments
    depthsCm (1,:) double
end

centimetersPerMeter = 100;

negativeDepths = depthsCm(depthsCm < 0);
if ~isempty(negativeDepths)
    error("gws:depthsToMeters:negativeDepth", ...
        "Abstichmaß darf nicht negativ sein, erhalten: %s", ...
        mat2str(negativeDepths));
end

depthsM = depthsCm / centimetersPerMeter;
end
```

## Abschlussprüfung

Vor jeder Übergabe ausführen und das Ergebnis wörtlich berichten:

1. `matlab -batch "buildtool check test"`

Ohne Build Tool einzeln:

1. `matlab -batch "issues = codeIssues('src'); disp(issues.Issues)"`
2. `matlab -batch "results = runtests('tests'); assertSuccess(results)"`

Schlägt eine Prüfung fehl oder konnte sie nicht laufen, steht das in der ersten Zeile der Übergabe. Ist in der Sitzung kein MATLAB verfügbar, wird das ausdrücklich gesagt. Code wird nie als geprüft bezeichnet, wenn die Prüfung nicht gelaufen ist.

## Herkunft der Regeln

Werkzeuge und Konfiguration wurden am 2026-10-05 nachgeschlagen. Die Angabe zur Formatierung im Editor stammt aus dem Wissensstand des Assistenten und ist zu prüfen.

| Herkunft | Regeln |
|---|---|
| MATLAB Coding Standards von MathWorks (Repository `matlab/rules`) | Benennung, Länge der Namen, `arguments`-Block, Formatierung, Kommentare, Fehlerbehandlung, zu vermeidende Funktionen |
| Dokumentation von MathWorks zum Build Tool | `buildfile.m`, `CodeIssuesTask`, `TestTask`, Aufruf `buildtool` |
| `sprach-codex`, gemeinsame Grundsätze | Grenzwerte, Trennung von Berechnung und Ein-/Ausgabe, Abschlussprüfung |
| Ergänzung für Messdaten | Einheiten im Namen, Dezimalkomma, Zeitzone, Toleranz bei Gleitkommazahlen |