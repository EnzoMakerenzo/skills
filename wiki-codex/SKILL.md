---
name: "wiki-codex"
description: "Regeln für ein vom Agenten gepflegtes Themen-Wiki aus bestätigten Rohquellen nach dem Muster LLM Wiki: Bestandsprüfung, Aufnehmen, Abfragen, Prüfen. Verwenden, wenn zu einem Thema ein Wiki aus Literatur aufgebaut, erweitert, befragt oder auf Konsistenz geprüft werden soll, und immer, wenn im Arbeitsordner ein Ordner wiki mit index.md liegt. Nicht verwenden für Literatursuche und Bewertung von Quellen, dafür gilt literatur-codex, nicht für Fließtext einer Arbeit, dafür gilt schreib-codex, und nicht für eigene Notizen, Messdaten oder Protokolle. Vorrang: literatur-codex entscheidet, welche Quelle bestätigt ist; Vorgaben der Betreuung gehen vor."
---

# Wiki-Codex: Themen-Wiki aus bestätigten Quellen

## Zweck

Wer zu einem Thema dreißig Quellen gelesen hat, sucht dieselbe Zahl beim Schreiben immer wieder neu. Dieser Codex lässt den Agenten das Gelesene einmal verdichten und danach aktuell halten: als Wiki aus Markdown-Seiten, das zwischen Enzo und den Rohquellen steht. Vorbild ist das Muster „LLM Wiki“ von Andrej Karpathy. Enzo wählt die Quellen und stellt die Fragen, der Agent fasst zusammen, verknüpft und führt Buch.

Das Wiki ist ein Arbeitsmittel und kein Beleg. Zitiert wird in jeder Arbeit die Rohquelle, nie eine Wiki-Seite.

## Grundregeln

1. **Rohquellen sind unveränderlich.** Der Agent liest sie, er ändert, verschiebt und benennt sie nie um.
2. **Nur bestätigte Quellen.** Aufgenommen wird, was in `quellenliste.md` den Status `bestätigt` trägt. Über den Status entscheidet Enzo nach `literatur-codex`.
3. **Keine Aussage ohne Beleg.** Jede Aussage nennt die Quellenseite und die Seitenzahl der Rohquelle. Was der Agent aus eigenem Wissen ergänzt, trägt den Vermerk `unbelegt`.
4. **Nur im Wiki-Ordner schreiben.** Außerhalb davon verändert der Agent keine Datei.
5. **Widersprüche bleiben sichtbar.** Weichen zwei Quellen voneinander ab, stehen beide Aussagen mit Beleg nebeneinander. Der Agent glättet nicht und entscheidet nicht.
6. **Das Wiki bleibt privat.** Es enthält Auszüge aus geschützten Werken und gehört in kein öffentliches Repository.

## Aufbau

```
<Arbeitsordner>/
  <Quellenordner>/      Rohquellen, nur lesen
  wiki/
    index.md            Verzeichnis aller Seiten
    log.md              Protokoll, wird nur fortgeschrieben
    quellenliste.md     Rohquellen mit Status
    quellen/            eine Seite je Rohquelle
    begriffe/           eine Seite je Begriff, Methode oder Größe
    vergleiche/         Gegenüberstellungen und gespeicherte Antworten
```

| Datei | Inhalt | Geändert bei |
|---|---|---|
| `index.md` | je Seite ein Wikilink und ein Satz, gegliedert nach Quellen, Begriffen, Vergleichen | jeder Aufnahme |
| `log.md` | je Vorgang ein Eintrag `## [JJJJ-MM-TT] aufnahme \| <Kurzbeleg>`, ebenso `abfrage`, `pruefung`, `bestaetigung` | jedem Vorgang |
| `quellenliste.md` | Tabelle: Datei, Kurzbeleg, Status, Lesestatus, aufgenommen am | Bestätigung und Aufnahme |

Dateinamen sind klein geschrieben, ohne Umlaute und Leerzeichen. Eine Quellenseite heißt `<erstautor>-<jahr>-<stichwort>.md`. Die Sprache der Seiten legt Enzo beim Anlegen fest. Fachbegriffe stehen beim ersten Auftreten zusätzlich in der Sprache der Quelle.

## Bestandsprüfung beim Start

Vor jedem anderen Vorgang stellt der Agent fest, ob im Arbeitsordner ein Wiki liegt. Merkmal ist `wiki/index.md`.

| Lage | Verhalten |
|---|---|
| Kein Wiki | Aufbau und Quellenordner vorschlagen, nach Sprache fragen, erst nach Enzos Bestätigung anlegen |
| Wiki vorhanden | zuerst den Prüflauf ausführen und das Ergebnis berichten, danach den gewünschten Vorgang |
| Wiki vorhanden, aber anders aufgebaut | Abweichungen als Liste melden und fragen: übernehmen oder daneben neu beginnen |

Fehlt `log.md`, `quellenliste.md` oder tragen die Seiten keine Belege, gilt das Wiki als anders aufgebaut. Der Agent baut ein fremdes Wiki nicht ungefragt um.

## Quellen bestätigen

- Der Agent trägt jede Datei des Quellenordners mit dem Status `Kandidat` in `quellenliste.md` ein.
- Auf `bestätigt` setzt er den Status nur nach Enzos ausdrücklicher Antwort. Bestätigt Enzo mehrere Quellen auf einmal, kommt ein Eintrag `bestaetigung` mit Datum und Zahl der Quellen in `log.md`.
- Lesestatus nach `literatur-codex`: `Zusammenfassung`, `Agent gelesen`, `Enzo gelesen`. Eine Aufnahme setzt ihn auf `Agent gelesen`, mehr nie.
- Kann der Agent eine Datei nicht oder nur teilweise lesen, etwa einen Scan ohne Textebene, nimmt er sie nicht auf und meldet sie.

## Aufnehmen

Eine Quelle je Durchgang, solange Enzo nichts anderes verlangt.

| Schritt | Handlung |
|---|---|
| 1 | Status in `quellenliste.md` prüfen. Ohne `bestätigt` ablehnen und melden |
| 2 | Die Quelle vollständig lesen. Bei Teilen festhalten, welche Seiten gelesen wurden |
| 3 | Quellenseite nach der Vorlage schreiben |
| 4 | Begriffsseiten ergänzen oder anlegen. Jede neue Aussage bekommt ihren Beleg |
| 5 | Widersprüche zu vorhandenen Aussagen auf der Begriffsseite unter „Widersprüche“ eintragen |
| 6 | `index.md`, `quellenliste.md` und `log.md` fortschreiben |
| 7 | Enzo berichten: neue Seiten, geänderte Seiten, Widersprüche, offene Punkte |

Eine Begriffsseite entsteht erst, wenn ein Begriff in der Quelle erklärt oder mit Zahlen belegt wird. Eine bloße Erwähnung genügt nicht.

## Seitenformate

Jede Seite beginnt mit Eigenschaften:

```
---
typ: <quelle | begriff | vergleich>
erzeugt_von: agent
erstellt: JJJJ-MM-TT
geaendert: JJJJ-MM-TT
quellen: [<Namen der Quellenseiten>]
---
```

Quellenseite:

```
Datei: <Dateiname im Quellenordner>
Kurzbeleg: <Autoren, Jahr, Titel, Digital Object Identifier>
Lesestatus: <Zusammenfassung | Agent gelesen | Enzo gelesen>
Gelesen: <vollständig | Seiten von bis>
Kernaussagen: <drei bis fünf Sätze in eigenen Worten, je mit Seite>
Methode: <wie die Ergebnisse zustande kamen, mit Seite>
Zahlen: <Werte mit Einheit, Bedingungen, Seite>
Zweifel: <was unklar oder strittig ist>
Begriffe: <Wikilinks auf die berührten Begriffsseiten>
```

Begriffsseite: eine Definition in zwei Sätzen, darunter die Abschnitte „Aussagen“, „Zahlen“, „Widersprüche“ und „Verwandte Begriffe“. Jede Zeile endet mit ihrem Beleg.

Form des Belegs: `([[quellen/<name>]], S. 12)`. Fehlt die Seitenzahl, weil die Quelle keine hat, steht der Abschnitt oder die Nummer der Abbildung.

- Zahlen stehen nie ohne Einheit und Bedingung, also Messgröße, Material, Bereich.
- Wörtlich übernommen wird höchstens ein Satz je Quelle, in Anführungszeichen und mit Seite. Abbildungen und Tabellen werden beschrieben, nicht kopiert.
- Angaben zu Autoren, Jahr und Titel stammen aus der Datei selbst, nie aus dem Gedächtnis.

## Abfragen

1. Zuerst `index.md` lesen, dann die passenden Seiten, bei Bedarf die Rohquelle an der belegten Stelle.
2. Die Antwort nennt je Aussage den Beleg in der Form der Rohquelle: Kurzbeleg und Seite.
3. Gibt das Wiki keine Antwort her, sagt der Agent das. Er füllt die Lücke nicht aus eigenem Wissen. Ergänzt er dennoch etwas, steht `unbelegt` dabei.
4. Eine Antwort, die Enzo behalten will, wird als Seite in `vergleiche/` gespeichert und in `index.md` eingetragen.
5. Jede Abfrage bekommt einen Eintrag in `log.md`.

Übernimmt Enzo eine Aussage in einen Text, gilt `schreib-codex`: Er prüft die Stelle in der Rohquelle und zitiert diese.

## Prüfen

Der Prüflauf ist bei der Bestandsprüfung und auf Wunsch derselbe. Zusätzlich läuft er nach jeder fünften Aufnahme.

| Nr. | Prüfvorgabe |
|---|---|
| 1 | Jede Seite steht in `index.md`, jeder Eintrag in `index.md` zeigt auf eine vorhandene Seite |
| 2 | Jede Aussage hat einen Beleg mit Quellenseite und Seitenzahl, oder sie ist als `unbelegt` gekennzeichnet |
| 3 | Jede zitierte Rohquelle liegt im Quellenordner und steht in `quellenliste.md` mit dem Status `bestätigt` |
| 4 | Aussagen verschiedener Seiten zum selben Sachverhalt widersprechen einander nicht, oder der Widerspruch ist benannt |
| 5 | Keine Seite ist verwaist, kein Wikilink zeigt ins Leere |
| 6 | `log.md` enthält für jede aufgenommene Quelle einen Eintrag mit Datum |
| 7 | Rohquellen, die seit der letzten Prüfung neu sind, geändert wurden oder fehlen, sind aufgelistet |

- Das Ergebnis ist eine Liste: je Prüfvorgabe „bestanden“ oder die Funde mit Seite und Zeile.
- Vorgabe 4 prüft der Agent an den Zahlen und Kernaussagen der Begriffsseiten, bei Stichproben nennt er deren Umfang.
- Der Prüflauf ändert nichts. Der Agent schlägt je Fund eine Korrektur vor und führt sie erst nach Enzos Freigabe aus.
- Jeder Prüflauf bekommt einen Eintrag in `log.md` mit der Zahl der Funde je Vorgabe.

## Arbeiten mit lokalen Modellen

Der Codex braucht nur das Lesen und Schreiben von Dateien. Unter pi mit einem lokalen Modell gilt zusätzlich:

- Kann das Modell PDF-Dateien nicht lesen, wandelt der Agent sie mit einem vorhandenen Werkzeug in Text um und legt den Text außerhalb des Quellenordners ab. Fehlt ein solches Werkzeug, meldet er das und nimmt nichts auf.
- Passt eine Quelle nicht in das Kontextfenster, liest er sie abschnittsweise und hält auf der Quellenseite fest, welche Seiten gelesen sind.
- Eine Seite, die ein kleineres Modell geschrieben hat, trägt dessen Namen in der Eigenschaft `erzeugt_von`.

## Abschlussprüfung

Vor jeder Übergabe an Enzo:

- [ ] Die Bestandsprüfung ist gelaufen, ihr Ergebnis steht am Anfang der Übergabe.
- [ ] Aufgenommen wurden nur Quellen mit dem Status `bestätigt`.
- [ ] Jede neue Aussage hat einen Beleg mit Seite oder den Vermerk `unbelegt`.
- [ ] `index.md`, `quellenliste.md` und `log.md` sind fortgeschrieben.
- [ ] Keine Datei außerhalb des Wiki-Ordners wurde verändert.
- [ ] Widersprüche, nicht lesbare Dateien und offene Punkte stehen an erster Stelle der Übergabe.

## Herkunft der Regeln

| Abschnitt | Herkunft |
|---|---|
| Drei Ebenen, unveränderliche Rohquellen, Vorgänge Aufnehmen, Abfragen, Prüfen, `index.md` und `log.md`, gespeicherte Antworten | extern: [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), Andrej Karpathy, 2026-04-04, Revision 1 |
| Status `bestätigt`, Lesestatus, Felder der Quellenseite | `literatur-codex` |
| Zitieren der Rohquelle statt der Wiki-Seite | `schreib-codex` |
| Bestandsprüfung, sieben Prüfvorgaben, Belegpflicht mit Seite, Vermerk `unbelegt`, Schreiben nur im Wiki-Ordner, `quellenliste.md`, Ordner und Dateinamen, Grenze für wörtliche Übernahmen, Arbeiten mit lokalen Modellen | Festlegung im Projekt KarpathyLLM, ohne externe Quelle |
