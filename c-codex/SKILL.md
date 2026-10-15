---
name: "c-codex"
description: "Regeln für sauberen C-Code auf Mikrocontrollern (ESP32, ESP-IDF, FreeRTOS) mit Grenzwerten, Werkzeugen und Abschlussprüfung. Verwenden bei jedem Schreiben, Ändern oder Prüfen von C-Code."
---

# C-Codex: Regeln für sauberen Code auf Mikrocontrollern

## Zweck

C auf einem Mikrocontroller verzeiht wenig: Ein Speicherfehler stürzt nicht ab, sondern fährt den Roboter gegen die Wand. Die Regeln zielen darauf, dass Enzo den Code in einem Jahr ohne Rückfrage versteht, dass Fehler an der Stelle auffallen, an der sie entstehen, und dass die Rechenlogik ohne Hardware testbar ist. Grenzwerte sind Richtwerte: Eine Abweichung ist erlaubt, wenn sie in einer Zeile begründet wird.

Rangfolge bei Widerspruch: Konventionen des bestehenden Projekts, dann die ESP-IDF-Stilrichtlinie, dann dieser Codex, dann BARR-C:2018. Für das Vorgehen vor dem ersten Code gilt `projekt-codex`, für Git `git-codex`. Einen Fach-Skill für ESP32 gibt es derzeit nicht; Plattformdetails kommen aus der ESP-IDF-Dokumentation der verwendeten Version.

## Werkzeuge

| Aufgabe | Werkzeug | Aufruf |
|---|---|---|
| Formatierung | astyle_py (ESP-IDF-Regeln) | `astyle_py --rules=tools/astyle-rules.yml <dateien>` |
| Statische Prüfung | cppcheck über PlatformIO | `pio check -e esp32s3 --fail-on-defect=medium` |
| Warnungen | GCC | `-Wall -Wextra -Werror` nur auf eigene Quellen |
| Tests | Unity über PlatformIO | `pio test -e native` |
| Übersetzen | PlatformIO | `pio run -e esp32s3` |

Grundkonfiguration in `platformio.ini`:

```ini
[env]
check_tool = cppcheck
check_flags = cppcheck: --enable=warning,style,performance,portability --inline-suppr
check_severity = medium, high
check_skip_packages = yes
check_src_filters = +<src/> +<components/> +<lib/>

[env:esp32s3]
platform = espressif32
framework = espidf
board = esp32-s3-devkitc-1
build_src_flags = -Wall -Wextra -Werror -Wshadow -Wformat=2 -Wundef

[env:native]
platform = native
test_framework = unity
build_src_flags = -Wall -Wextra -Werror -Wshadow -Wconversion
```

Die Formatierungsregeln entsprechen `tools/ci/astyle-rules.yml` aus ESP-IDF: `--style=otbs --indent=spaces=4 --convert-tabs --align-pointer=name --pad-header --pad-oper --unpad-paren --max-code-length=120`. Die genauen Optionen werden beim Anlegen des Projekts gegen die ESP-IDF-Version geprüft (Wissensstand des Assistenten). Was ein Werkzeug erzwingt, wird nicht von Hand diskutiert. `// cppcheck-suppress` nur mit Begründung in derselben Zeile.

## Benennung

- Namen sagen, was der Wert bedeutet: `left_speed_pct` statt `v1`.
- Physikalische Größen tragen die Einheit im Namen: `wheel_diameter_mm`, `loop_period_ms`, `battery_voltage_mv`.
- Funktionen und Variablen in `snake_case`, Makros und Aufzählungswerte in `UPPER_SNAKE_CASE`, Typen mit Endung `_t`.
- Öffentliche Namen tragen das Komponentenpräfix: `motor_set_speed()`, `line_sensor_read()`, `MOTOR_MAX_DUTY`.
- Dateilokale Variablen sind `static` und beginnen mit `s_`. Globale Variablen über Modulgrenzen gibt es nicht.
- Unterbrechungsroutinen enden auf `_isr`, Wahrheitswerte beginnen mit `is_`, `has_` oder `should_`.
- Bezeichner auf Englisch, Kommentare auf Deutsch.

## Funktionen

- Eine Funktion erledigt eine Aufgabe. Braucht die Beschreibung ein "und", wird geteilt.
- Richtwerte: höchstens 30 Anweisungen, höchstens 4 Parameter, Verschachtelung höchstens 3 Ebenen.
- Mehr als 4 zusammengehörige Parameter werden zu einer `struct`, übergeben als `const`-Zeiger.
- Keine booleschen Schalterparameter. Stattdessen zwei Funktionen oder ein `enum`.
- Frühe Rückgabe statt tiefer Verschachtelung. Kein `goto`, außer für einen einzigen Aufräumpfad am Funktionsende.
- Alles, was nur in einer Datei gebraucht wird, ist `static`.
- Zeigerparameter, die nur gelesen werden, sind `const`.

## Struktur

- Je Komponente ein Verzeichnis unter `components/<name>/` mit `include/<name>.h`, `<name>.c` und `CMakeLists.txt`. `main/` enthält nur Start und Verdrahtung der Komponenten.
- Rechnen und Hardware sind getrennt: Reine Rechenlogik (Regler, Kalibrierung, Sensorauswertung) steht in Dateien ohne ESP-IDF-Includes und läuft im `native`-Test. Hardwarezugriff steht in einer dünnen Schicht darüber.
- Abhängigkeiten zeigen nur nach unten: `app` → `controller` → `line_sensor`, `motor` → ESP-IDF-Treiber. Keine Komponente kennt `app`.
- Kopfdateien beginnen mit `#pragma once` und `extern "C"`-Klammer. Sie enthalten nur, was andere Module brauchen.
- Include-Reihenfolge: C-Standardbibliothek, POSIX, FreeRTOS, ESP-IDF, eigene Komponenten, je Gruppe durch Leerzeile getrennt.
- Keine magischen Zahlen: benannte Konstanten mit Einheit (`static const` oder `#define`). Pinbelegung und Abstimmwerte stehen gesammelt in einer Konfigurationsdatei oder in Kconfig.
- Dateien bis etwa 400 Zeilen, ein Thema je Datei.

## Typen und Speicher

- Ganzzahlen mit fester Breite aus `<stdint.h>` (`int32_t`, `uint8_t`), wo die Breite zählt. `bool` aus `<stdbool.h>`, `size_t` für Größen.
- Vorzeichenbehaftete und vorzeichenlose Werte werden nicht in einem Ausdruck gemischt.
- Gleitkommazahlen nie auf Gleichheit prüfen, sondern mit Toleranz. `float` statt `double`, weil die FPU des ESP32-S3 nur einfache Genauigkeit rechnet.
- Kein `malloc` nach dem Start. Speicher, Warteschlangen und Aufgaben werden in der Startphase angelegt, bevorzugt statisch (`xTaskCreateStatic`, `xQueueCreateStatic`).
- Puffergrößen sind Konstanten. Jeder Zugriff auf einen Puffer prüft die Grenze; Zeichenketten nur mit `snprintf`, nie mit `sprintf` oder `strcpy`.
- Bitfelder nur in vorzeichenlosen Typen und nie zur Abbildung von Registern.

## Fehlerbehandlung

- Funktionen, die scheitern können, geben `esp_err_t` zurück. Ergebnisse gehen über einen Ausgabezeiger als letzten Parameter.
- Jeder Rückgabewert wird ausgewertet. Weitergeben mit `ESP_RETURN_ON_ERROR` oder `ESP_GOTO_ON_ERROR` aus `esp_check.h`.
- `ESP_ERROR_CHECK` nur in der Startphase in `app_main`, wo ein Fehler den Neustart rechtfertigt.
- `assert` nur für interne Logikfehler, nie für Eingaben oder Hardwarezustände.
- Eingaben am Anfang prüfen und `ESP_ERR_INVALID_ARG` zurückgeben. Die Logmeldung nennt den erhaltenen Wert und die Erwartung.
- Protokoll mit `ESP_LOGE`, `ESP_LOGW`, `ESP_LOGI`, `ESP_LOGD` und einem `static const char *TAG` je Datei. Kein `printf`.
- Jedes `switch` hat einen `default`-Zweig, auch wenn er nur einen Fehler meldet.

## Besonderheiten Mikrocontroller und FreeRTOS

- Unterbrechungsroutinen sind kurz: Wert sichern, Aufgabe benachrichtigen, fertig. Kein Logging, kein Warten, keine Gleitkommarechnung. Speicherort mit `IRAM_ATTR`.
- Daten, die eine Unterbrechungsroutine und eine Aufgabe teilen, sind `volatile` und werden mit kritischem Abschnitt oder atomar gelesen.
- Zwischen Aufgaben werden Daten über Warteschlangen oder Benachrichtigungen ausgetauscht, nicht über gemeinsame Variablen.
- Jede Aufgabe hat eine benannte Stapelgröße, Priorität und Periode. Periodische Aufgaben verwenden `vTaskDelayUntil`, nicht `vTaskDelay`, damit die Regelschleife nicht driftet.
- Keine Warteschleifen mit leerem Körper. Wartezeiten in Ticks über `pdMS_TO_TICKS`.
- Der Watchdog bleibt aktiv. Eine Aufgabe, die ihn auslöst, ist ein Fehler, kein Einstellungsproblem.
- Motoren gehen bei jedem Fehler, Neustart und Verbindungsverlust in einen sicheren Zustand (Stillstand).

## Tests

- Jedes Arbeitspaket bringt seine Tests mit.
- Rechenlogik wird mit Unity in der Umgebung `native` auf dem Rechner getestet, ohne Hardware. Tests auf dem Gerät nur für die Hardwareschicht.
- Testdateien unter `test/test_<modul>/`, Testfunktionen `test_<was>_<bedingung>_<erwartung>`.
- Pflichtfälle: Normalfall, Nullwerte, Grenzwerte (kleinster und größter Wert, Überlauf), ungültige Eingabe mit erwartetem Fehlercode.
- Gleitkommaergebnisse mit `TEST_ASSERT_FLOAT_WITHIN` prüfen.

## Kommentare und Dokumentation

- Kommentare erklären das Warum, nicht das Was.
- Öffentliche Funktionen in der Kopfdatei mit Doxygen-Kommentar: `@brief`, `@param`, `@return` mit allen möglichen Fehlercodes.
- Einheiten und Wertebereiche stehen im Kommentar jedes Parameters.
- Kein auskommentierter Code, kein `TODO` ohne Issue-Nummer.

## Abhängigkeiten

- ESP-IDF und Plattformversion sind in `platformio.ini` festgeschrieben (`platform = espressif32@<version>`).
- Fremdkomponenten nur über den ESP-IDF Component Manager mit Versionsangabe in `idf_component.yml`. Jede neue Abhängigkeit wird mit einem Satz begründet.
- Arduino-Bibliotheken werden nicht verwendet.

## Beispiel

Schlecht:

```c
int spd(int l, int r, int f) {
    int x;
    if (f) x = l - r; else x = r - l;
    if (x > 255) x = 255;
    return x;
}
```

Gut:

```c
#define MOTOR_DUTY_MAX 255

/* Begrenzt den Stellwert, weil der Treiber nur 8 Bit Tastgrad annimmt. */
esp_err_t controller_clamp_duty(int32_t requested_duty, uint8_t *out_duty)
{
    if (out_duty == NULL) {
        return ESP_ERR_INVALID_ARG;
    }
    if (requested_duty < 0) {
        *out_duty = 0;
    } else if (requested_duty > MOTOR_DUTY_MAX) {
        *out_duty = MOTOR_DUTY_MAX;
    } else {
        *out_duty = (uint8_t)requested_duty;
    }
    return ESP_OK;
}
```

## Abschlussprüfung

Vor jeder Übergabe ausführen und das Ergebnis wörtlich berichten:

1. `astyle_py --rules=tools/astyle-rules.yml <geänderte Dateien>`
2. `pio run -e esp32s3`
3. `pio check -e esp32s3 --fail-on-defect=medium`
4. `pio test -e native`

Schlägt eine Prüfung fehl oder konnte sie nicht laufen, steht das in der ersten Zeile der Übergabe. Code wird nie als geprüft bezeichnet, wenn die Prüfung nicht gelaufen ist. Tests auf dem Gerät werden getrennt berichtet.

## Herkunft der Regeln

| Regelgruppe | Quelle |
|---|---|
| Format, Benennung, Kopfdateien, Include-Reihenfolge | ESP-IDF Espressif IoT Development Framework Style Guide, Version 6.1 |
| Fehlermodell, `esp_check.h`, Logging | ESP-IDF Programming Guide, Error Handling und Logging |
| Statische Prüfung | PlatformIO-Dokumentation, Static Code Analysis (`check_*`-Optionen) |
| Klammern, `volatile`, ISR-Namen, feste Breiten, `default`, Vorzeichenmischung, Gleitkommavergleich, `static` | BARR-C:2018, Regeln 1.3.a, 1.7.c, 1.8.a, 1.8.c, 5.2.a, 5.3.c, 5.4.b, 6.5.b, 8.3.b |
| Grenzwerte, Trennung Rechnen und Ein-/Ausgabe | gemeinsame Grundsätze aus `sprach-codex` |
| Kein dynamischer Speicher nach dem Start, FreeRTOS-Regeln | FreeRTOS-Dokumentation zu statischer Allokation; Wissensstand des Assistenten, zu prüfen |