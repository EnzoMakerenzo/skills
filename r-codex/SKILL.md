---
name: "r-codex"
description: "Regeln für sauberen R-Code mit Grenzwerten, Werkzeugen (Air, lintr, testthat, renv) und Abschlussprüfung. Verwenden bei jedem Schreiben, Ändern oder Prüfen von R-Code, auch in Quarto- und R-Markdown-Dokumenten. Nicht verwenden bei reinen Statistikfragen, bei denen kein Code entsteht. Vorrang: gilt nach projekt-codex und zusätzlich zu git-codex."
---

# R-Codex: Regeln für sauberen Code

## Zweck

Auswertungen in R werden oft einmal geschrieben und Jahre später wieder gebraucht. Die Regeln zielen darauf, dass Enzo oder eine Kollegin eine Auswertung in einem Jahr ohne Rückfrage versteht, erneut ausführt und dasselbe Ergebnis erhält. Grenzwerte sind Richtwerte: Eine Abweichung ist erlaubt, wenn sie in einer Zeile begründet wird.

Vorhandene Konventionen eines bestehenden Projekts haben Vorrang vor diesem Codex. Für das Vorgehen vor dem ersten Code gilt `projekt-codex`, für die Versionsverwaltung `git-codex`.

## Werkzeuge

| Aufgabe | Werkzeug | Aufruf |
|---|---|---|
| Formatierung | Air | `air format .` |
| Formatierung nur prüfen | Air | `air format . --check` |
| Statische Prüfung | lintr | `Rscript -e 'lintr::lint_dir(".")'` |
| Tests | testthat, 3. Ausgabe | `Rscript -e 'testthat::test_dir("tests/testthat")'` |
| Abhängigkeiten | renv | `Rscript -e 'renv::status()'` |

R hat keine statische Typprüfung. Ihren Platz nimmt die Eingabeprüfung am Anfang jeder Funktion ein, siehe Abschnitt Typen.

Was ein Werkzeug erzwingt, wird nicht von Hand diskutiert. Air braucht für die Vorgaben unten keine Konfiguration, weil sie seinen Standardwerten entsprechen (Zeilenlänge 80, Einrückung 2 Leerzeichen, Zuweisung mit `<-`). Grundkonfiguration `.lintr` im Projektordner:

```
linters: linters_with_defaults(
    line_length_linter(80L),
    cyclocomp_linter(10L),
    object_name_linter(styles = c("snake_case", "SNAKE_CASE", "symbols")),
    object_length_linter(40L)
  )
encoding: UTF-8
exclusions: list("renv")
```

`cyclocomp_linter` braucht das Paket `cyclocomp`. Die Grenzwerte für Anweisungen, Parameter und Verschachtelung prüft lintr nicht, sie werden beim Review geprüft.

## Benennung

- Namen sagen, was der Wert bedeutet, nicht welchen Typ er hat: `groundwater_level_m` statt `df2`.
- Schreibweise `snake_case` für Variablen und Funktionen, `SNAKE_CASE` für Konstanten.
- Ausgeschriebene Wörter. Ausnahmen: Laufvariablen in Schleifen bis drei Zeilen und in der Statistik übliche Zeichen (`n`, `p`, `x`, `y`) innerhalb einer Formel.
- Physikalische Größen tragen die Einheit im Namen: `depth_cm`, `conductivity_us_per_cm`, `duration_s`. Das gilt auch für Spaltennamen in Tabellen.
- Funktionen heißen nach dem, was sie tun (Verb), Wahrheitswerte beginnen mit `is_`, `has_` oder `should_`.
- Bezeichner auf Englisch, Kommentare und Dokumentation auf Deutsch.
- Keine Namen, die Funktionen aus Basis-R überdecken: `data`, `df`, `c`, `t`, `mean`.

## Funktionen

- Eine Funktion erledigt eine Aufgabe. Braucht die Beschreibung ein "und", wird geteilt.
- Richtwerte: höchstens 30 Anweisungen, höchstens 4 Parameter, Verschachtelung höchstens 3 Ebenen.
- Mehr als 4 zusammengehörige Parameter werden zu einer benannten Liste, die eine eigene Funktion erzeugt und prüft.
- Keine booleschen Schalterparameter, die das Verhalten umschalten. Stattdessen zwei Funktionen.
- Optionale Parameter stehen hinter den Pflichtparametern und werden beim Aufruf mit Namen übergeben.
- Frühe Rückgabe statt tiefer Verschachtelung. `return()` nur für die frühe Rückgabe, am Ende steht der Wert als letzter Ausdruck.
- Berechnung und Ein-/Ausgabe trennen: Funktionen, die rechnen, lesen keine Dateien, schreiben keine und zeichnen keine Diagramme.
- Eine Pipe-Kette hat höchstens etwa 10 Schritte. Längere Ketten werden an einer fachlich sinnvollen Stelle in benannte Zwischenergebnisse geteilt.

## Struktur

| Ordner | Inhalt |
|---|---|
| `R/` | Funktionen, ein Thema je Datei, bis etwa 300 Zeilen |
| `scripts/` | nummerierte Einstiegsskripte: `01_import.R`, `02_clean.R`, `03_analyse.R` |
| `data/raw/` | Rohdaten, nur lesen |
| `data/processed/` | abgeleitete Daten |
| `output/` | Diagramme, Tabellen, Berichte |
| `tests/testthat/` | Tests |

- Skripte enthalten nur den Ablauf: Funktionen laden, aufrufen, Ergebnis speichern. Die Fachlogik liegt in `R/`.
- Alle `library()`-Aufrufe stehen am Anfang des Skripts, nie in einer Funktion. In Funktionen unter `R/` wird mit `paket::funktion()` aufgerufen.
- Kein `setwd()`, kein `attach()`, kein `rm(list = ls())`. Pfade entstehen relativ zum Projektordner mit `here::here()` oder `file.path()`, nie als zusammengesetzte Zeichenketten.
- Keine veränderlichen globalen Zustände, kein `<<-`. Konfiguration an einer Stelle als benannte Liste.
- Keine magischen Zahlen: benannte Konstanten mit Einheit.
- Der Arbeitsbereich wird beim Beenden nicht gespeichert und beim Start nicht geladen (`.RData` aus).

## Typen

- Jede Funktion prüft ihre Eingaben in den ersten Zeilen: Typ, Länge, Wertebereich. Mittel: `stopifnot()` mit benannten Bedingungen oder eine ausdrückliche Prüfung mit `stop()`.
- `TRUE` und `FALSE` ausschreiben, nie `T` und `F`.
- Typstabile Funktionen: `vapply()` oder `purrr::map_dbl()` und Verwandte statt `sapply()`.
- `seq_along(x)` und `seq_len(n)` statt `1:length(x)`, weil die Schleife sonst bei leerer Eingabe zweimal läuft.
- Beim Einlesen werden Spaltentypen ausdrücklich angegeben (`col_types`), nicht geraten. Faktoren entstehen nur ausdrücklich und mit festgelegten Stufen.
- Fehlende Werte sind `NA` und werden an genau einer Stelle behandelt.

## Fehlerbehandlung

- Fehler mit `stop(..., call. = FALSE)` auslösen. Die Meldung nennt den erhaltenen Wert und die Erwartung.
- `tryCatch()` fängt nur bestimmte Bedingungen und löst Unbekanntes erneut aus. Kein leerer `error`-Zweig.
- Fehler und Warnungen nie stillschweigend schlucken: kein `suppressWarnings()` und kein `try(silent = TRUE)` ohne Kommentar, welche Warnung warum unbedenklich ist.
- Übersprungene Datensätze werden gezählt und gemeldet.
- Früh scheitern: Eingaben am Anfang prüfen, nicht mitten in der Berechnung.
- Meldungen mit `message()` oder `warning()`, nicht mit `print()` oder `cat()`.

## Daten und Reproduzierbarkeit

- Rohdaten werden nie überschrieben. Ergebnisse gehen in eigene Dateien.
- Koordinatenbezugssystem, Zeitzone und Einheit immer ausdrücklich setzen und prüfen, nie annehmen: `sf::st_crs()`, `tz =` bei jeder Zeitumwandlung.
- Dezimaltrennzeichen und Spaltentrenner beim Einlesen ausdrücklich angeben. Dateien aus österreichischen Systemen haben oft Strichpunkt und Dezimalkomma: `readr::read_csv2()` oder `locale(decimal_mark = ",")`.
- `na.rm = TRUE` nur mit Kommentar, warum Fehlwerte hier entfallen dürfen, und mit gemeldeter Anzahl.
- Vor einer Statistik stehen die Annahmen des Verfahrens im Kommentar und werden geprüft, zum Beispiel Unabhängigkeit und Verteilung.
- Zufallszahlen mit `set.seed()` und festem Startwert.
- Berichte entstehen aus Quarto-Dokumenten, die nur Funktionen aus `R/` aufrufen. Zahlen im Text werden berechnet, nicht abgetippt.

## Tests

- Jedes Arbeitspaket bringt seine Tests mit.
- Getestet wird Verhalten, nicht die innere Umsetzung.
- Dateien heißen `test-<thema>.R`, die Beschreibung in `test_that()` nennt Gegenstand, Bedingung und Erwartung.
- Pflichtfälle: Normalfall, leere Eingabe, `NA`, Grenzwerte, ungültige Eingabe.
- Gleitkommazahlen mit `expect_equal()` und Toleranz vergleichen, nie mit `==`.
- Kein Netzwerk und keine echten Produktivdaten in Tests. Kleine Beispieldateien unter `tests/testthat/data/`.

## Kommentare und Dokumentation

- Kommentare erklären das Warum, nicht das Was.
- Jede Funktion unter `R/` hat einen roxygen2-Kommentar mit Kurzbeschreibung, `@param` je Parameter mit Einheit und `@return`.
- Kein auskommentierter Code, keine Notiz ohne Kontext.

## Abhängigkeiten

- Basis-R zuerst. Jedes neue Paket wird mit einem Satz begründet.
- Versionen werden mit renv festgeschrieben: `renv::init()` am Anfang, `renv::snapshot()` nach jeder Änderung. `renv.lock` gehört ins Repository, der Ordner `renv/library` nicht.
- Die R-Version wird aus dem Projekt übernommen. In neuen Projekten die aktuelle stabile Version.

## Beispiel

Schlecht:

```r
f <- function(d, f = T) {
  r <- c()
  for (i in 1:length(d)) {
    if (d[i] > 0) {
      if (f) r <- c(r, d[i] * 0.01) else r <- c(r, d[i])
    }
  }
  r
}
```

Gut:

```r
CENTIMETERS_PER_METER <- 100

#' Rechnet Abstichmaße von Zentimeter in Meter um.
#'
#' @param depths_cm Numerischer Vektor, Abstichmaße in Zentimeter, nicht negativ.
#' @return Numerischer Vektor gleicher Länge, Abstichmaße in Meter.
depths_to_meters <- function(depths_cm) {
  stopifnot("depths_cm muss numerisch sein" = is.numeric(depths_cm))
  negative_depths <- depths_cm[!is.na(depths_cm) & depths_cm < 0]
  if (length(negative_depths) > 0) {
    stop(
      "Abstichmaß darf nicht negativ sein, erhalten: ",
      toString(negative_depths),
      call. = FALSE
    )
  }
  depths_cm / CENTIMETERS_PER_METER
}
```

## Abschlussprüfung

Vor jeder Übergabe ausführen und das Ergebnis wörtlich berichten:

1. `air format .`
2. `Rscript -e 'lintr::lint_dir(".")'`
3. `Rscript -e 'testthat::test_dir("tests/testthat")'`
4. `Rscript -e 'renv::status()'`

Schlägt eine Prüfung fehl oder konnte sie nicht laufen, steht das in der ersten Zeile der Übergabe. Code wird nie als geprüft bezeichnet, wenn die Prüfung nicht gelaufen ist.

## Herkunft der Regeln

Werkzeuge und Konfiguration wurden am 2026-10-05 nachgeschlagen.

| Herkunft | Regeln |
|---|---|
| Tidyverse Style Guide | Benennung, Zuweisung, Zeilenlänge, Pipe, Rückgabe |
| Dokumentation von Air (Posit) | Aufrufe, Standardwerte der Formatierung |
| Dokumentation von lintr 3.4.0 | Aufbau der Datei `.lintr`, Prüfregeln |
| Dokumentation von testthat und renv | Tests, festgeschriebene Versionen |
| `sprach-codex`, gemeinsame Grundsätze | Grenzwerte, Trennung von Berechnung und Ein-/Ausgabe, Fehlerbehandlung, Abschlussprüfung |
| Ergänzung für Messdaten | Einheiten im Namen, Dezimalkomma, Zeitzone, Koordinatenbezugssystem |