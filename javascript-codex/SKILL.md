---
name: "javascript-codex"
description: "Regeln für sauberen JavaScript-Code (Node.js, Code-Knoten in n8n) mit Grenzwerten, Werkzeugen und Abschlussprüfung. Verwenden bei jedem Schreiben, Ändern oder Prüfen von JavaScript-Code."
---

# JavaScript-Codex: Regeln für sauberen Code

## Zweck

JavaScript entsteht bei Enzo vor allem an zwei Orten: als Code-Knoten in n8n-Workflows und als Skripte und Tests unter Node.js. Die Regeln zielen darauf, dass beides ohne Rückfrage verständlich bleibt und dass Logik aus Workflows außerhalb von n8n prüfbar ist. Grenzwerte sind Richtwerte: Eine Abweichung ist erlaubt, wenn sie in einer Zeile begründet wird.

Vorhandene Konventionen eines bestehenden Projekts haben Vorrang vor diesem Codex, etwa deutsche Bezeichner in einem Repository, das sie bereits durchgehend verwendet. Für das Vorgehen vor dem ersten Code gilt `projekt-codex`, für Git `git-codex`. TypeScript in Angular regelt `angular-codex`.

## Einfachheit zuerst

Diese Regeln gehen allen anderen Abschnitten vor.

- Die einfachste Lösung, die die Anforderung erfüllt, wird gewählt. Einfach heißt leicht zu lesen, nicht möglichst kurz.
- Nichts auf Vorrat: Eine Abstraktion, Klasse oder Konfigurationsmöglichkeit entsteht erst beim zweiten tatsächlichen Bedarf.
- Zwischen zwei gleichwertigen Lösungen gewinnt die mit weniger Code, weniger Dateien und weniger Abhängigkeiten.
- Funktionen und einfache Objekte zuerst. `class` nur, wenn Daten und Verhalten zusammengehören.
- Eingebaute Mittel von Node.js zuerst (`node:test`, `node:assert`, `node:fs`). Ein npm-Paket nur mit Begründung in einem Satz.
- Keine verketteten Ausdrücke über mehr als drei Methoden, keine verschachtelten ternären Ausdrücke.

## Werkzeuge

| Aufgabe | Werkzeug | Aufruf |
|---|---|---|
| Formatierung und statische Prüfung | Biome | `npx biome check --write .` |
| Prüfung ohne Änderung | Biome | `npx biome ci .` |
| Tests | Node.js Test Runner | `node --test` |

Biome ersetzt Prettier und ESLint mit einem einzigen Werkzeug ohne weitere Abhängigkeiten. Die Version wird mit `npm i -D -E @biomejs/biome` in `package.json` festgeschrieben. Grundkonfiguration `biome.json`:

```json
{
  "formatter": { "indentStyle": "space", "indentWidth": 2, "lineWidth": 100 },
  "linter": {
    "rules": {
      "recommended": true,
      "complexity": {
        "noExcessiveCognitiveComplexity": { "level": "error", "options": { "maxAllowedComplexity": 10 } }
      },
      "style": { "useConst": "error", "noParameterAssign": "error" }
    }
  },
  "javascript": { "formatter": { "quoteStyle": "double", "semicolons": "always" } }
}
```

Was ein Werkzeug erzwingt, wird nicht von Hand diskutiert. Eine Regel wird nur zeilenweise abgeschaltet, mit Grund: `// biome-ignore lint/<gruppe>/<regel>: <Grund>`.

Code-Knoten in n8n liegen als Text in JSON-Dateien und werden von Biome nicht erfasst. Für sie gilt der Abschnitt Code-Knoten in n8n und die Prüfung über Tests.

## Benennung

- Namen sagen, was der Wert bedeutet: `orderId` statt `x`.
- Variablen und Funktionen in camelCase, Konstanten auf Modulebene in UPPER_SNAKE_CASE, Klassen in PascalCase.
- Physikalische Größen und Zeiten tragen die Einheit im Namen: `timeoutMs`, `depthCm`.
- Funktionen heißen nach dem, was sie tun (Verb). Wahrheitswerte beginnen mit `is`, `has` oder `should`.
- Bezeichner auf Englisch, Kommentare auf Deutsch, soweit das Projekt nichts anderes durchgehend verwendet.
- Dateien in kebab-case, Module mit Endung `.mjs` oder `"type": "module"` in `package.json`.

## Funktionen

- Eine Funktion erledigt eine Aufgabe. Braucht die Beschreibung ein "und", wird geteilt.
- Richtwerte: höchstens 30 Anweisungen, höchstens 4 Parameter, Verschachtelung höchstens 3 Ebenen.
- Mehr als 4 zusammengehörige Parameter werden zu einem Objekt mit Destrukturierung.
- Keine booleschen Schalterparameter. Stattdessen zwei Funktionen.
- Frühe Rückgabe statt tiefer Verschachtelung.
- Berechnung und Ein-/Ausgabe trennen: Funktionen, die rechnen, lesen keine Dateien und rufen kein Netz.

## Struktur

- ES-Module (`import`/`export`), kein `require` in neuem Code.
- Module bis etwa 300 Zeilen, ein Thema je Modul.
- `const` als Regel, `let` nur bei Neuzuweisung, nie `var`.
- Kein veränderlicher globaler Zustand, keine magischen Zahlen: benannte Konstanten mit Einheit.
- Pfade mit `node:path` oder `new URL(..., import.meta.url)`, nie zusammengesetzte Zeichenketten.

## Code-Knoten in n8n

- Modus "Run Once for All Items" als Regel; Zugriff über `$input.first()`, `$input.all()` und `$('Knotenname')`. Rückgabe immer ein Feld von Objekten `{ json: ... }`.
- Ein Code-Knoten höchstens 50 Zeilen. Mehr Logik wird auf mehrere Knoten mit sprechenden Namen verteilt.
- Kein Dateizugriff und kein HTTP im Code-Knoten; dafür gibt es eigene Knoten. Module nur, soweit `NODE_FUNCTION_ALLOW_BUILTIN` sie erlaubt.
- Zugangsdaten kommen aus Zugangsdaten von n8n oder aus `$env`, nie als Text im Workflow.
- Jeder Knoten mit Entscheidungslogik wird getestet: Der Test liest den Code aus der Workflow-Datei, führt ihn mit `new Function("$", "$input", "$env", code)` aus und ersetzt `$input`, `$env` und `$` durch kleine Attrappen.
- Workflows werden als JSON im Repository versioniert. Was in n8n läuft, entspricht dem Stand im Repository; Änderungen in der Oberfläche werden exportiert und committet.

## Typen

- Daten an Systemgrenzen (Antworten von Schnittstellen, Dateien, Telegram) werden beim Einlesen geprüft: Typ, Pflichtfelder, erlaubte Werte.
- Vergleiche mit `===` und `!==`. Fehlende Werte mit `??` behandeln, nicht mit `||`, wenn `0` oder `""` gültig sind.
- Typen für Funktionen mit nicht offensichtlicher Form stehen als JSDoc (`@param`, `@returns`).

## Fehlerbehandlung

- Fehler werden mit `throw new Error(...)` gemeldet. Die Meldung nennt den erhaltenen Wert und die Erwartung.
- Kein leerer `catch`. Wer fängt, behandelt oder wirft mit Zusammenhang weiter (`{ cause }`).
- Jedes `Promise` wird erwartet oder ausdrücklich behandelt; keine schwebenden Aufrufe.
- Früh scheitern: Eingaben am Anfang prüfen.

## Besonderheiten

- Node.js-Version aus dem Projekt übernehmen; Code läuft mindestens mit der ältesten Version der Zielumgebung (pibox: Node.js 22).
- `JSON.parse` nur auf Daten, die genau JSON sein sollen, etwa die Standardausgabe eines Adapters, nicht Standardausgabe und Fehlerausgabe zusammen.
- Zeiten in UTC verarbeiten, Zeitzone nur bei der Ausgabe setzen.

## Tests

- Rahmenwerk: `node:test` mit `node:assert/strict`, Dateien `tests/<thema>.test.mjs`.
- Testnamen beschreiben Verhalten: `<was> <bedingung> <erwartung>`.
- Pflichtfälle: Normalfall, leere Eingabe, Fehlwerte, Grenzwerte, ungültige Eingabe.
- Kein Netz, keine echten Zugangsdaten, keine Produktivdaten.

## Kommentare und Dokumentation

- Kommentare erklären das Warum, nicht das Was.
- Exportierte Funktionen tragen einen JSDoc-Kommentar mit Zweck, `@param`, `@returns` und `@throws`.
- Jeder Code-Knoten beginnt mit einer Kommentarzeile zu seiner Aufgabe.
- Kein auskommentierter Code.

## Abhängigkeiten

- Standardbibliothek von Node.js zuerst. Jede neue Abhängigkeit wird mit einem Satz begründet.
- Versionen mit `npm i -E` festschreiben, `package-lock.json` committen.

## Beispiel

Schlecht:

```js
function check(d, strict) {
  try {
    var o = JSON.parse(d);
    if (o.u == 'ok' || !strict) return o;
  } catch (e) {}
}
```

Gut:

```js
const ALLOWED_VERDICTS = ["annehmen", "aendern", "blockieren"];

/**
 * Liest das Prüfurteil aus der Antwort eines Adapters.
 * @param {string} stdout Standardausgabe des Adapters, genau eine JSON-Zeile.
 * @returns {{verdict: string}} das geprüfte Urteil.
 * @throws {Error} wenn die Ausgabe kein JSON ist oder das Urteil fehlt.
 */
export function parseVerdict(stdout) {
  let answer;
  try {
    answer = JSON.parse(stdout);
  } catch (error) {
    throw new Error(`Ausgabe ist kein JSON: ${stdout.slice(0, 120)}`, { cause: error });
  }
  if (!ALLOWED_VERDICTS.includes(answer.urteil)) {
    throw new Error(`Urteil '${answer.urteil}' unbekannt, erwartet: ${ALLOWED_VERDICTS.join(", ")}`);
  }
  return { verdict: answer.urteil };
}
```

## Abschlussprüfung

Vor jeder Übergabe ausführen und das Ergebnis wörtlich berichten:

1. `npx biome check --write .`
2. `npx biome ci .`
3. `node --test`
4. `jq empty workflows/*.json`, wenn das Projekt n8n-Workflows enthält

Schlägt eine Prüfung fehl oder konnte sie nicht laufen, steht das in der ersten Zeile der Übergabe. Code wird nie als geprüft bezeichnet, wenn die Prüfung nicht gelaufen ist.

## Herkunft der Regeln

| Herkunft | Regeln |
|---|---|
| [Biome Quick start](https://biomejs.dev/guides/getting-started/) - Abruf 2026-11-03 - Version 2.6.4 | Werkzeug, Festschreiben mit `-E`, `biome check`, `biome.json` |
| [Biome CLI](https://biomejs.dev/reference/cli/) - Abruf 2026-11-03 | `biome ci` für die Prüfung ohne Änderung |
| [Node.js Test runner](https://nodejs.org/api/test.html) - Abruf 2026-11-03 | `node:test`, Aufruf `node --test` |
| [n8n: Using the Code node](https://docs.n8n.io/code/code-node/) - Abruf 2026-11-03 | Modi des Code-Knotens, kein Dateizugriff und kein HTTP, Module bei Selbstbetrieb |
| `sprach-codex`, gemeinsame Grundsätze | Einfachheit zuerst, Richtwerte für Funktionen, Fehlermeldungen, Pflichtfälle der Tests, Abschlussprüfung |
| Ergänzung für Enzos Umgebung | Code-Knoten höchstens 50 Zeilen, Tests der Knoten über `new Function`, Workflows im Repository, Node.js 22 in der pibox |

Die Schalter der Regeln in `biome.json` (`noExcessiveCognitiveComplexity`, `useConst`, `noParameterAssign`) stammen aus dem Wissensstand des Assistenten und sind vor der ersten Verwendung mit `npx biome check` zu prüfen.
