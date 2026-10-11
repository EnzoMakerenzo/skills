---
name: "bash-codex"
description: "Regeln für sauberen Bash-Code mit Grenzwerten, Werkzeugen und Abschlussprüfung. Verwenden bei jedem Schreiben, Ändern oder Prüfen von Bash-Code."
---

# Bash-Codex: Regeln für sauberen Code

## Zweck

Shell-Skripte laufen oft mit weiten Rechten und ohne Aufsicht. Die Regeln zielen darauf, dass ein Skript beim ersten Fehler anhält, statt mit halbem Zustand weiterzulaufen, und dass Enzo es in einem Jahr ohne Rückfrage versteht. Grenzwerte sind Richtwerte: Eine Abweichung ist erlaubt, wenn sie in einer Zeile begründet wird.

Vorhandene Konventionen eines bestehenden Projekts haben Vorrang vor diesem Codex. Für das Vorgehen vor dem ersten Code gilt `projekt-codex`, für Git `git-codex`.

Bash ist die richtige Wahl für das Verketten von Programmen und für Startskripte. Braucht ein Skript Datenstrukturen, Rechnen mit Kommazahlen oder mehr als etwa 200 Zeilen, wird es in Python geschrieben.

## Werkzeuge

| Aufgabe | Werkzeug | Aufruf |
|---|---|---|
| Formatierung | shfmt | `shfmt -w -i 2 -ci -bn .` |
| Statische Prüfung | ShellCheck | `shellcheck -x bin/* tests/*.bash` |
| Tests | bats-core | `bats tests` |

Was ein Werkzeug erzwingt, wird nicht von Hand diskutiert. Grundkonfiguration in `.shellcheckrc` im Wurzelordner:

```
shell=bash
enable=require-variable-braces
enable=quote-safe-variables
enable=check-unassigned-uppercase
external-sources=true
```

Eine Meldung von ShellCheck wird nur zeilenweise abgeschaltet, mit Nummer und Grund: `# shellcheck disable=SC2034  # wird von der eingebundenen Datei gelesen`.

## Benennung

- Namen sagen, was der Wert bedeutet: `project_dir` statt `d`.
- Variablen und Funktionen in Kleinbuchstaben mit Unterstrich: `mount_args`, `read_config`.
- Konstanten und exportierte Umgebungsvariablen in Großbuchstaben, mit `readonly` festgelegt: `readonly IMAGE_NAME="pibox"`.
- Physikalische Größen tragen die Einheit im Namen: `timeout_s`, `size_mb`.
- Funktionen heißen nach dem, was sie tun (Verb). Prüffunktionen beginnen mit `is_` oder `has_` und antworten über den Rückgabewert.
- Bezeichner auf Englisch, Kommentare auf Deutsch.
- Ausführbare Skripte ohne Endung in `bin/`, eingebundene Bibliotheken mit Endung `.bash`.

## Funktionen

- Eine Funktion erledigt eine Aufgabe. Braucht die Beschreibung ein "und", wird geteilt.
- Richtwerte: höchstens 30 Anweisungen, höchstens 4 Parameter, Verschachtelung höchstens 3 Ebenen.
- Jede Variable in einer Funktion ist `local`. Deklaration und Zuweisung aus einer Befehlsersetzung stehen in getrennten Zeilen, sonst verdeckt `local` den Rückgabewert.
- Parameter werden in der ersten Zeile benannt: `local config_path="${1}"`.
- Keine Schalterparameter wie `true` oder `false`, die das Verhalten umschalten. Stattdessen zwei Funktionen.
- Ergebnisse gehen über die Standardausgabe, Erfolg oder Misserfolg über den Rückgabewert. Meldungen an Menschen gehen auf die Fehlerausgabe.
- Frühe Rückgabe statt tiefer Verschachtelung.

## Struktur

- Erste Zeile `#!/usr/bin/env bash`, danach ein Kopfkommentar mit Zweck und Aufruf, danach `set -euo pipefail`.
- Reihenfolge in der Datei: Konstanten, Funktionen, am Ende `main "$@"`. Außerhalb von Funktionen steht kein weiterer ausführender Code.
- `main` liest Argumente und ruft Funktionen auf. Funktionen, die etwas zusammensetzen oder prüfen, führen selbst nichts aus. So bleiben sie testbar.
- Kein veränderlicher globaler Zustand. Globale Namen sind `readonly`.
- Keine magischen Zahlen und keine verstreuten Pfade: benannte Konstanten am Anfang.
- Skripte bis etwa 200 Zeilen. Gemeinsame Funktionen wandern in eine Bibliothek, die mit `source` eingebunden wird.

## Typen und Speicher

Bash kennt nur Zeichenketten, Ganzzahlen und Felder. Umso wichtiger ist der Umgang mit Leerzeichen und fehlenden Werten.

- Jede Variable wird in Anführungszeichen und mit geschweiften Klammern verwendet: `"${project_dir}"`.
- Listen sind Felder, nie durch Leerzeichen getrennte Zeichenketten: `mount_args+=("--volume" "${path}:${path}:ro")`, Verwendung mit `"${mount_args[@]}"`.
- Befehle werden als Feld zusammengesetzt und ausgeführt. `eval` ist verboten.
- Fehlende Werte ausdrücklich behandeln: `"${VAULT_DIR:-}"` mit anschließender Prüfung oder `"${VAULT_DIR:?VAULT_DIR ist nicht gesetzt}"`.
- Bedingungen mit `[[ ... ]]`, Rechnen mit `(( ... ))`, Befehlsersetzung mit `$(...)`.
- Zeilen werden mit `while IFS= read -r line` gelesen, nie mit `for line in $(cat datei)`.
- Temporäre Dateien entstehen mit `mktemp` und werden über `trap` beim Beenden entfernt.

## Fehlerbehandlung

- `set -euo pipefail` gilt in jedem Skript. Es ersetzt keine Prüfung: Eingaben und Voraussetzungen werden am Anfang von `main` ausdrücklich geprüft.
- Fehlermeldungen gehen auf die Fehlerausgabe und nennen den erhaltenen Wert und die Erwartung: `die "Projektordner nicht gefunden: '${project_dir}', erwartet ein bestehender Ordner"`.
- Eine Funktion `die` gibt die Meldung aus und beendet mit einem Wert ungleich null. Rückgabewerte: 0 Erfolg, 1 Laufzeitfehler, 2 falscher Aufruf.
- Fehler werden nie mit `|| true` oder `2>/dev/null` verschluckt. Ist ein Fehlschlag erwartet, steht der Grund im Kommentar daneben.
- Benötigte Programme werden am Anfang mit `command -v` geprüft.
- Aufräumarbeiten laufen über `trap cleanup EXIT`.
- Zerstörende Befehle (`rm -r`, `mv` über bestehende Ziele) erhalten nur geprüfte, nicht leere, absolute Pfade.

## Besonderheiten

- Zielversion ist die Bash des Zielsystems. Unter macOS ist die mitgelieferte Bash 3.2: Skripte, die auch dort laufen sollen, verzichten auf assoziative Felder und `mapfile` oder prüfen die Version am Anfang.
- Kein `cd` ohne Prüfung. Besser mit absoluten Pfaden arbeiten oder `cd` in einer Unterschale.
- Kein Auswerten der Ausgabe von `ls`. Dateien werden mit Mustern oder `find -print0` durchlaufen.
- `sudo` steht nie im Skript. Braucht ein Schritt erhöhte Rechte, wird das Skript mit Hinweis beendet.
- Zugangsdaten stehen nie im Skript und nie in der Befehlszeile, sondern kommen aus der Umgebung oder einer Datei außerhalb des Repositorys.
- Zeilenlänge höchstens 80 Zeichen. Lange Befehle werden mit einem Feld oder mit Zeilenfortsetzung umbrochen.

## Tests

- Jedes Arbeitspaket bringt seine Tests mit, als Dateien `tests/<thema>.bats`.
- Getestet wird Verhalten: Ausgabe, Rückgabewert, angelegte Dateien.
- Testnamen: `<was> <bedingung> <erwartung>`, zum Beispiel `@test "read_config ohne Datei meldet Fehler und endet mit 1"`.
- Pflichtfälle: Normalfall, leere Eingabe, Pfad mit Leerzeichen, fehlende Datei, ungültiges Argument.
- Tests arbeiten in einem Ordner aus `mktemp -d` und verändern nichts außerhalb. Kein Netzwerk.
- Externe Programme mit Nebenwirkung, etwa `docker`, werden im Test durch ein Ersatzprogramm im `PATH` vertreten, das seine Argumente aufzeichnet.

## Kommentare und Dokumentation

- Kommentare erklären das Warum, nicht das Was.
- Jede Funktion, die nicht selbsterklärend ist, hat einen Kopfkommentar mit Zweck, Argumenten, Ausgabe und Rückgabewert.
- Jedes Skript beantwortet `--help` mit Zweck, Aufruf und Beispiel.
- Kein auskommentierter Code, keine Notiz ohne Kontext.

## Abhängigkeiten

- Zuerst die eingebauten Mittel der Bash und die Grundprogramme des Systems. Jedes weitere Programm wird mit einem Satz begründet und am Anfang geprüft.
- Versionen der Prüfwerkzeuge stehen in der Anleitung des Projekts.

## Beispiel

Schlecht:

```bash
#!/bin/bash
d=$1
for f in `ls $d`; do
  cp $d/$f /backup 2>/dev/null
done
```

Gut:

```bash
#!/usr/bin/env bash
# Kopiert alle Dateien eines Ordners in den Sicherungsordner.
# Aufruf: backup_files <quellordner>
set -euo pipefail

readonly BACKUP_DIR="/backup"

die() {
  printf 'Fehler: %s\n' "${1}" >&2
  exit "${2:-1}"
}

# Kopiert jede Datei aus dem Quellordner in den Sicherungsordner.
# Argumente: Quellordner. Rückgabe: 0 bei Erfolg.
copy_files() {
  local source_dir="${1}"
  local file_path
  for file_path in "${source_dir}"/*; do
    # Ein leerer Ordner liefert das Muster selbst zurück.
    [[ -e "${file_path}" ]] || continue
    cp -- "${file_path}" "${BACKUP_DIR}/"
  done
}

main() {
  [[ $# -eq 1 ]] || die "erwartet genau ein Argument, erhalten: $#" 2
  local source_dir="${1}"
  [[ -d "${source_dir}" ]] \
    || die "Quellordner nicht gefunden: '${source_dir}'"
  [[ -d "${BACKUP_DIR}" ]] \
    || die "Sicherungsordner nicht gefunden: '${BACKUP_DIR}'"
  copy_files "${source_dir}"
}

main "$@"
```

## Abschlussprüfung

Vor jeder Übergabe ausführen und das Ergebnis wörtlich berichten:

1. `shfmt -d -i 2 -ci -bn .`
2. `shellcheck -x bin/* tests/*.bash`
3. `bats tests`

Schlägt eine Prüfung fehl oder konnte sie nicht laufen, steht das in der ersten Zeile der Übergabe. Code wird nie als geprüft bezeichnet, wenn die Prüfung nicht gelaufen ist.

## Herkunft der Regeln

| Herkunft | Regeln |
|---|---|
| [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html) | Benennung, `main`, `local`, Felder, Anführungszeichen, Einrückung mit 2 Leerzeichen, Zeilenlänge 80, Grenze für den Wechsel zu einer anderen Sprache |
| [ShellCheck Wiki](https://www.shellcheck.net/wiki/) | Verbot von `eval` und Auswerten von `ls`, getrennte Deklaration bei `local`, zeilenweises Abschalten mit Grund |
| [GNU Bash Reference Manual](https://www.gnu.org/software/bash/manual/) | `set -euo pipefail`, `trap`, Parametererweiterung mit Vorgabe und Pflichtwert |
| [bats-core Dokumentation](https://bats-core.readthedocs.io/) | Aufbau und Aufruf der Tests |
| `sprach-codex`, gemeinsame Grundsätze | Richtwerte für Funktionen, Fehlermeldungen, Pflichtfälle der Tests, Abschlussprüfung |
| Ergänzung für Enzos Umgebung | Bash 3.2 unter macOS, Verbot von `sudo` im Skript, Ersatzprogramme für `docker` in Tests |

Stand der Werkzeuge beim Entwurf am 2026-10-11: shfmt 3.13, bats-core 1.14. Die Versionen sind vor der ersten Verwendung am Zielsystem zu prüfen.
