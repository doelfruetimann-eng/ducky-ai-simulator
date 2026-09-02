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
