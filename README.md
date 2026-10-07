# skills

Eigene Skills für Claude, ein Ordner je Skill mit einer `SKILL.md`.

Dieses Verzeichnis ist Sicherung und Historie. Wirksam ist die im Konto gespeicherte Fassung; nach jeder Änderung an einem Skill wird die gespeicherte Fassung hierher übernommen.

| Skill | Zweck |
|---|---|
| `projekt-codex` | Vorgehen bei Programmiervorhaben: Konzept, Entwurf, Umsetzung, Abnahme, Abschluss |
| `git-codex` | Repository, Branches, Commits, Review |
| `python-codex` | Codequalität für Python |
| `sprach-codex` | Codex für Sprachen ohne eigenen Codex |
| `r-codex` | Codequalität für R |
| `matlab-codex` | Codequalität für MATLAB |
| `literatur-codex` | Forschungsfrage, Literatursuche, Bewertung von Quellen, Exzerpt, Literaturverzeichnis |

Die Übersicht, wann welcher Skill greift, steht in Obsidian: `TechStack/Skill-Index.md`.

## Skills in anderen Sprachmodellen verwenden

Jeder Skill ist eine einzelne Markdown-Datei im offenen Format [Agent Skills](https://agentskills.io): oben ein Kopf mit `name` und `description`, darunter die Regeln als Text. Deshalb lässt er sich auch außerhalb von Claude verwenden. Der Weg hat drei Schritte: herunterladen, personalisieren, einfügen.

### 1. Herunterladen

```
git clone https://github.com/EnzoMakerenzo/skills.git
```

Ohne Git: auf GitHub über "Code" und "Download ZIP". Für einen einzelnen Skill genügt dessen Datei `SKILL.md`.

### 2. Bearbeiten und personalisieren

Die Skills sind auf meine Arbeitsweise zugeschnitten. Vor der Verwendung wird die `SKILL.md` in einem Texteditor geöffnet und angepasst. Die Suche nach den Begriffen der ersten Spalte findet die Stellen.

| Suchbegriff | Bedeutung im Skill | Anpassen auf |
|---|---|---|
| `Enzo` | Person, die Fragen beantwortet, prüft und freigibt | den eigenen Namen |
| `Obsidian` | Ablageort für Projektdokumente und Notizen | das eigene Notizwerkzeug oder einen Ordner |
| `Wiener Neustadt` | Lehrveranstaltungen, aus denen die Regeln stammen | eigene Vorgaben, oder die Herkunftsangabe streichen |
| `IEEE` | Standard für den Zitierstil | den verlangten Zitierstil |
| `-codex` | Verweis auf einen anderen Skill dieser Sammlung | den genannten Skill mit übernehmen oder den Verweis streichen |

- Die `description` im Kopf legt fest, wann ein Modell den Skill von selbst lädt. Wer die Auslöser ändern will, ändert diesen Satz.
- Der `name` im Kopf und der Name des Ordners müssen übereinstimmen. Wer einen Skill umbenennt, ändert beide.
- Grenzwerte und Werkzeuge in den Codizes der Sprachen, zum Beispiel in `python-codex`, lassen sich an die eigenen Gewohnheiten anpassen.

### 3. Einfügen

**Weg A: per Drag and Drop in den Chat.** Das funktioniert in jeder Chat-Oberfläche mit Dateianhang, auch bei lokal betriebenen Modellen.

1. Die bearbeitete `SKILL.md` in das Chatfenster ziehen.
2. Dazuschreiben: "Arbeite in diesem Chat nach den Regeln der angehängten Datei."
3. Bei mehreren Skills die Dateien vorher umbenennen, zum Beispiel in `python-codex.md`, weil sonst alle `SKILL.md` heißen.

Die Datei gilt nur für diesen einen Chat. Dauerhaft wirkt sie, wenn sie in einem Projekt, in einem eigenen Assistenten oder im Systemprompt hinterlegt ist. Nimmt eine Oberfläche die Endung `.md` nicht an, hilft das Umbenennen in `.txt` oder das Einfügen des Inhalts als Text.

**Weg B: als Skill installieren.** Werkzeuge mit Skill-Funktion laden den Skill von selbst, sobald die Aufgabe zur `description` passt.

| Werkzeug | Vorgehen |
|---|---|
| Claude (Web und Desktop) | Ordner des Skills als ZIP packen und in den Einstellungen im Bereich Skills hochladen |
| Claude Code | Ordner des Skills nach `~/.claude/skills/` kopieren |
| ChatGPT | im Bereich Skills über "Create" und "Upload from your computer" hochladen; nur in den Tarifen Business, Enterprise, Healthcare und Edu, sonst Weg A |
| Gemini CLI | Ordner des Skills nach `~/.gemini/skills/` kopieren |
| pi | Ordner des Skills nach `~/.pi/agent/skills/` kopieren oder den Pfad des Repositorys in `settings.json` unter `skills` eintragen |

Menüs und Tarife ändern sich. Maßgeblich sind die Anleitungen der Hersteller: [Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude), [ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt), [Gemini CLI](https://geminicli.com/docs/cli/skills), [pi](https://pi.dev/docs/latest/skills).

### Grenzen

- Ein Modell ohne Werkzeuge befolgt die Regeln nur im Text. Schritte wie Git-Befehle, Tests oder das Ablegen von Notizen führt es nicht selbst aus, sondern beschreibt sie.
- Die Skills verweisen aufeinander. `projekt-codex` setzt zum Beispiel `git-codex` und den Codex der jeweiligen Sprache voraus.
- Bei kleinen lokalen Modellen nur den Skill einfügen, der für die Aufgabe gebraucht wird, damit das Kontextfenster reicht.
