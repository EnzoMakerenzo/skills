---
name: "angular-codex"
description: "Regeln für einfachen, sauberen Angular-Code mit Grenzwerten, Werkzeugen und Abschlussprüfung. Verwenden bei jedem Schreiben, Ändern oder Prüfen von Angular-Code, also TypeScript, Vorlagen und Stilen in einem Angular-Projekt."
---

# Angular-Codex: Regeln für einfachen, sauberen Code

## Zweck

Angular bietet für fast jedes Problem mehrere Wege. Die Regeln wählen jeweils den einfachsten, damit Enzo den Code in einem Jahr ohne Rückfrage versteht und gefahrlos ändert. Grenzwerte sind Richtwerte: Eine Abweichung ist erlaubt, wenn sie in einer Zeile begründet wird.

Vorhandene Konventionen eines bestehenden Projekts haben Vorrang vor diesem Codex. Für das Vorgehen vor dem ersten Code gilt `projekt-codex`, für Git `git-codex`.

## Einfachheit zuerst

Diese Regeln gehen allen anderen Abschnitten vor.

- Die einfachste Lösung, die die Anforderung erfüllt, wird gewählt. Einfach heißt leicht zu lesen, nicht möglichst kurz.
- Nichts auf Vorrat: Ein Service, ein Interface, eine Basisklasse oder ein generischer Typ entsteht erst beim zweiten tatsächlichen Verwender.
- Zustand mit Signalen (`signal`, `computed`). RxJS nur, wo Ereignisströme verknüpft werden müssen, etwa Eingaben mit Verzögerung. Eine Bibliothek für Zustandsverwaltung (NgRx und ähnliche) nur mit schriftlicher Begründung im Entwurf.
- Daten vom Server mit `httpResource` oder `resource`, nicht mit selbst verwalteten Abonnements.
- Keine `NgModule`. Komponenten, Direktiven und Pipes sind eigenständig.
- Eine Komponente mit einer Datei für Vorlage und Stil, solange beide zusammen unter etwa 40 Zeilen bleiben. Darüber getrennte Dateien `.html` und `.css`.
- Zwischen zwei gleichwertigen Lösungen gewinnt die mit weniger Dateien, weniger Abhängigkeiten und weniger Angular-Begriffen.

## Werkzeuge

| Aufgabe | Werkzeug | Aufruf |
|---|---|---|
| Formatierung | Prettier | `npx prettier --write .` |
| Statische Prüfung | angular-eslint | `ng lint` |
| Typprüfung | TypeScript über den Build | `ng build` |
| Tests | Vitest über den Angular-Builder | `ng test --watch=false` |

Einrichtung im neuen Projekt: `ng new <name> --style=css --ssr=false`, danach `ng add angular-eslint`. Was ein Werkzeug erzwingt, wird nicht von Hand diskutiert. Grundkonfiguration:

```json
// tsconfig.json, Auszug
{
  "compilerOptions": {
    "strict": true,
    "noImplicitOverride": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noPropertyAccessFromIndexSignature": true
  },
  "angularCompilerOptions": {
    "strictTemplates": true,
    "strictInjectionParameters": true,
    "strictInputAccessModifiers": true
  }
}
```

In `eslint.config.js` werden zusätzlich gesetzt: `max-params` 4, `max-statements` 30, `max-depth` 3, `complexity` 10, `@typescript-eslint/no-explicit-any` als Fehler, `@angular-eslint/prefer-on-push-component-change-detection` und `@angular-eslint/template/prefer-control-flow`.

## Benennung

- Dateinamen in Kleinbuchstaben mit Bindestrich, benannt nach dem Inhalt: `well-list.ts`, `well-list.html`, `well-list.spec.ts`. Keine Sammeldateien wie `utils.ts` oder `helpers.ts`.
- Klassen in PascalCase, Variablen und Funktionen in camelCase, Konstanten in Großbuchstaben mit Unterstrich.
- Selektoren tragen das Kürzel des Projekts: `app-well-list`, Direktiven `[appHighlight]`.
- Physikalische Größen tragen die Einheit im Namen: `depthCm`, `durationS`.
- Ereignisbehandlungen heißen nach der Handlung, nicht nach dem Ereignis: `saveMeasurement()` statt `onClick()`.
- Wahrheitswerte beginnen mit `is`, `has` oder `should`.
- Bezeichner auf Englisch, Kommentare auf Deutsch.

## Funktionen

- Eine Funktion erledigt eine Aufgabe. Braucht die Beschreibung ein "und", wird geteilt.
- Richtwerte: höchstens 30 Anweisungen, höchstens 4 Parameter, Verschachtelung höchstens 3 Ebenen.
- Mehr als 4 zusammengehörige Parameter werden zu einem Objekt mit eigenem Typ.
- Keine booleschen Schalterparameter, die das Verhalten umschalten. Stattdessen zwei Funktionen.
- Frühe Rückgabe statt tiefer Verschachtelung.
- Berechnungen sind reine Funktionen in eigenen Dateien, ohne Angular-Abhängigkeit. So sind sie ohne `TestBed` testbar.

## Struktur

- Ordner nach Fachthema, nicht nach Art: `src/app/wells/`, nicht `src/app/components/`.
- Tests liegen neben dem Code, den sie prüfen.
- Ein Begriff je Datei: eine Komponente, ein Service oder eine Gruppe reiner Funktionen. Dateien bis etwa 200 Zeilen.
- Komponenten zeigen an, Services holen und halten Daten, reine Funktionen rechnen. Abhängigkeiten zeigen nur in diese Richtung.
- Komponenten gruppieren oben die Angular-Mitglieder (Abhängigkeiten, Eingaben, Ausgaben, Abfragen), darunter die Methoden.
- Keine Logik in der Vorlage über einen einfachen Vergleich hinaus. Abgeleitete Werte werden mit `computed` in der Klasse gebildet.
- Kein veränderlicher globaler Zustand außerhalb von Services. Konfiguration an einer Stelle, über `environment` oder ein `InjectionToken`.
- Keine magischen Zahlen: benannte Konstanten mit Einheit.

## Typen und Speicher

- Kein `any`. Unbekannte Daten sind `unknown` und werden vor der Verwendung geprüft.
- Antworten vom Server werden an der Grenze geprüft und in eigene Typen überführt, nicht ungeprüft als Typ behauptet.
- Fehlende Werte ausdrücklich als `T | undefined` und an genau einer Stelle behandeln. Kein `!` zum Abschalten der Prüfung.
- Abhängigkeiten mit `inject()`, nicht über den Konstruktor.
- Eingaben, Ausgaben und Abfragen mit `input()`, `output()`, `viewChild()` und als `readonly`.
- Mitglieder, die nur die Vorlage liest, sind `protected`. `public` nur für die echte Schnittstelle.
- Wo doch abonniert wird, endet das Abonnement mit `takeUntilDestroyed()`. Kein manuelles `subscribe` ohne Ende.

## Fehlerbehandlung

- Fehler nie stillschweigend schlucken. Kein leeres `catch`, kein `catchError(() => EMPTY)` ohne Meldung.
- Fehlerzustände von `httpResource` (`error()`) werden in der Vorlage sichtbar behandelt.
- Fehlermeldungen nennen den erhaltenen Wert und die Erwartung.
- Früh scheitern: Eingaben am Anfang prüfen, nicht mitten in der Berechnung.
- Kein `console.log` im übergebenen Code.

## Besonderheiten

- Änderungserkennung `OnPush`, ab Angular 22 Vorgabe. Neue Anwendungen laufen ohne Zone.js.
- Steuerfluss in Vorlagen mit `@if`, `@for` mit `track`, `@switch`, nicht mit `*ngIf` und `*ngFor`.
- Klassen und Stile mit `[class.name]` und `[style.eigenschaft]`, nicht mit `NgClass` und `NgStyle`.
- Formulare mit Signal Forms, ab Angular 22 stabil. In bestehenden Projekten bleibt die vorhandene Formularart.
- Lebenszyklusmethoden bleiben kurz und rufen benannte Methoden auf. Die passende Schnittstelle, etwa `OnInit`, wird angegeben.
- Zugangsdaten stehen nie im Code. Alles im Browser ist öffentlich.
- Stile mit einfachem CSS. Ein Präprozessor oder eine Komponentenbibliothek nur mit Begründung.

## Tests

- Jedes Arbeitspaket bringt seine Tests mit.
- Getestet wird Verhalten: was angezeigt wird und was nach einer Handlung geschieht, nicht innere Methoden.
- Reine Funktionen ohne `TestBed`, Komponenten mit `TestBed` und echtem Rendern.
- Testnamen beschreiben Bedingung und Erwartung: `it('zeigt Fehlermeldung bei leerer Eingabe')`.
- Pflichtfälle: Normalfall, leere Eingabe, Fehlwerte, Grenzwerte, ungültige Eingabe, Fehlerantwort des Servers.
- Kein echtes Netzwerk: `provideHttpClientTesting()` und `HttpTestingController`.

## Kommentare und Dokumentation

- Kommentare erklären das Warum, nicht das Was.
- TSDoc-Kommentare (`/** ... */`) für öffentliche Funktionen und Services, mit `@param`, `@returns`, `@throws`.
- Kein auskommentierter Code, keine Notiz ohne Kontext.

## Abhängigkeiten

- Angular und die Browserschnittstellen zuerst. Jede weitere Bibliothek wird mit einem Satz begründet.
- Versionen in `package.json` ohne `^` und `~`, `package-lock.json` liegt im Repository. Installation mit `npm ci`.
- Aktualisierung nur mit `ng update`, eine Hauptversion nach der anderen.

## Beispiel

Schlecht:

```typescript
@Component({
  selector: 'app-wells',
  template: `<div *ngFor="let w of data"><span *ngIf="w.d > 0">{{ w.d * 0.01 }}</span></div>`,
})
export class WellsComponent implements OnInit {
  data: any[] = [];
  constructor(private http: HttpClient) {}
  ngOnInit() {
    this.http.get<any[]>('/api/wells').subscribe((r) => (this.data = r));
  }
}
```

Gut:

```typescript
const CENTIMETERS_PER_METER = 100;

/** Rechnet ein Abstichmaß von Zentimeter in Meter um. */
export function depthToMeters(depthCm: number): number {
  if (depthCm < 0) {
    throw new RangeError(`Abstichmaß darf nicht negativ sein, erhalten: ${depthCm}`);
  }
  return depthCm / CENTIMETERS_PER_METER;
}

interface Well {
  readonly name: string;
  readonly depthCm: number;
}

@Component({
  selector: 'app-well-list',
  template: `
    @if (wells.error()) {
      <p>Messstellen konnten nicht geladen werden.</p>
    }
    @for (well of wells.value(); track well.name) {
      <p>{{ well.name }}: {{ toMeters(well.depthCm) }} m</p>
    }
  `,
})
export class WellList {
  protected readonly wells = httpResource<Well[]>(() => '/api/wells', { defaultValue: [] });
  protected readonly toMeters = depthToMeters;
}
```

## Abschlussprüfung

Vor jeder Übergabe ausführen und das Ergebnis wörtlich berichten:

1. `npx prettier --check .`
2. `ng lint`
3. `ng build`
4. `ng test --watch=false`

Schlägt eine Prüfung fehl oder konnte sie nicht laufen, steht das in der ersten Zeile der Übergabe. Code wird nie als geprüft bezeichnet, wenn die Prüfung nicht gelaufen ist.

## Herkunft der Regeln

| Herkunft | Regeln |
|---|---|
| [Angular Style Guide](https://angular.dev/style-guide) | Dateinamen, Ordner nach Fachthema, Tests neben dem Code, `inject()`, `protected` und `readonly`, `computed` statt Vorlagenlogik, Klassenbindungen, Namen der Ereignisbehandlungen, Lebenszyklusmethoden |
| [Angular-Dokumentation](https://angular.dev) | Signale, `httpResource`, Steuerfluss, `OnPush`, eigenständige Komponenten, `takeUntilDestroyed`, strenge Vorlagenprüfung, Testen mit `HttpTestingController` |
| [What's new in Angular 22.0](https://blog.ninja-squad.com/2026/06/03/what-is-new-angular-22.0) | `OnPush` als Vorgabe, Signal Forms und Resources stabil, TypeScript 6 |
| [angular-eslint](https://github.com/angular-eslint/angular-eslint) | Einrichtung mit `ng add`, Regeln zu `OnPush` und Steuerfluss |
| `sprach-codex`, gemeinsame Grundsätze | Einfachheit zuerst, Richtwerte für Funktionen, Fehlermeldungen, Pflichtfälle der Tests, Abschlussprüfung |
| Ergänzung für Enzos Arbeitsweise | Vorrang der Einfachheit vor Angular-Mustern, Vorlage in der Komponente bis 40 Zeilen, Begründungspflicht für Zustandsbibliotheken |

Stand beim Entwurf am 2026-10-15: Angular 22. Vitest als Vorgabe für neue Projekte und Betrieb ohne Zone.js stammen aus dem Wissensstand des Assistenten und sind vor der ersten Verwendung mit `ng version` und der Dokumentation zu prüfen.
