# Engineer-Vertrag (Stand 2026-09-02, geschaerft)

Quelle der Wahrheit: Git doelfruetimann-eng/ducky-ai-simulator.
Entscheidet: Doelf anhand von Messergebnissen.

Alle Engines duerfen Dateien anlegen, MuJoCo laufen lassen und Tests schreiben.
Getrennt wird nach Verantwortung und Gegenkontrolle, nicht nach Schreibrecht.

## Verantwortung

- Grok: Gegenvarianten, Physik-Skepsis, CH-Kosten, kippt/lohnt sich nicht. Review: Codex + Fable 5.1
- Codex/ChatGPT: Integration, Vergleich, Test-Harness. Review: Grok + Claude Code
- Claude Code + Opus 5: Alltag im Checkout, Refactor, wiederholbare Skripte. Review: Codex
- Fable 5.1: Architektur-Review, blockierende Entscheidungen. Doelf liest das Review
- Doelf: Merge, Kauf, Training nach der Tabelle

## Kontrolle

Wer eine Variante vorschlaegt, schreibt nicht allein 'bestanden'.
Zweite Engine laesst tip_test.py nochmals laufen.
Keine Pollen-STLs. Masse nicht schoenrechnen. Mini = Viewer, 4060/HF = Training.

## AKV Claude Code + Opus 5 (abgelegt 2026-09-02)

Nachgelesen im Repo, nicht aus dem Gedaechtnis. Fundstelle je Zeile, damit die
naechste Session nicht wieder fragen muss. Quellen: CLAUDE.md (fa7df2c),
dieser Vertrag, docs/GIT.md, docs/LOOP.md, docs/BOARD.md.

### Aufgaben

| Was | Fundstelle |
|---|---|
| Alltag im Checkout, Refactor, wiederholbare Skripte | ENGINEERS.md, Abschnitt Verantwortung |
| Implementation und Skripte als Schwerpunkt | CLAUDE.md |
| Gegenkontrolle fuer Codex (eine seiner zwei Review-Instanzen) | ENGINEERS.md, Abschnitt Verantwortung |
| Als zweite Engine tip_test.py nochmals laufen lassen | ENGINEERS.md, Abschnitt Kontrolle |
| Nach jeder COM-Aenderung tip_test.py laufen lassen | CLAUDE.md |
| Hoechstens drei Umlaeufe, dann Doelf; Ergebnis nach COMPARE.md oder reviews/ | LOOP.md |

### Kompetenzen

Dateien anlegen, MuJoCo laufen lassen, Tests schreiben — ohne exklusives
Schreibrecht (CLAUDE.md, ENGINEERS.md). Getrennt wird nach Verantwortung und
Gegenkontrolle, nicht danach, wer welche Datei anfassen darf.
Arbeitsgebiet: models/, tests/, docs/ (CLAUDE.md).
Zweig claude/*, von dort PR nach develop (GIT.md).

### Grenzen (ausdruecklich verboten)

- Keine Pollen-STLs committen
- D_full nicht schoenrechnen, Masse nicht verstecken
- Kein Warp-Training auf dem Mac mini (Mini = Viewer, 4060/HF = Training)
- Beine und Schnabel nicht neu als CAD (CLAUDE.md fa7df2c)
- A-D nicht loeschen (CLAUDE.md); A-F vollstaendig halten (Doelf, 02.09.2026)
- Nicht allein "bestanden" schreiben
- main, Merge, Kauf und Training sind Doelfs

### Verantwortung

Review durch Codex. Entscheidungen: Doelf anhand von Messergebnissen.
Ich bin nicht mein eigener Pruefer. Nichts gilt, was nur im Chat steht —
Commit auf develop mit Pfad und SHA (CLAUDE.md, Abschnitt "Ablegen ist Pflicht").

### Entschieden und offen

- **CAD entschieden:** Der Streit vom Board (16:15, Codex "Claude leitet CAD
  inkl. Gehaeuse, Beine, Schnabel" gegen Grok "nur CadQuery-Zubehoer") ist mit
  CLAUDE.md fa7df2c zugunsten von Grok entschieden: Beine und Schnabel nicht
  neu als CAD. Kein CAD im Repo, dabei bleibt es bis Doelf etwas anderes sagt.
- **Offen:** CLAUDE.md schreibt "A-D nicht loeschen", Doelf sagte am 02.09.2026
  "A-F nicht loeschen". Die BASELINE in tests/tip_test.py haelt alle sechs, also
  die schaerfere Fassung. Wenn CLAUDE.md A-D meint und E/F absichtlich
  freigibt, muss die BASELINE angepasst werden — ich aendere das nicht von mir
  aus. Frage an Doelf.
