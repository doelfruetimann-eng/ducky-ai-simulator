# COMPARE A-F (Grok 2026-09-02, Codex bitte gegenlesen)

Gleiche Stoesse: Ruhe / 2.5 N Seite / 3 N hinten, 1200 Schritte.

| Modell | kg | COM z | Ruhe | Seite | Hinten | Neu ca. |
|---|---|---|---|---|---|---|
| A_stock | 0.80 | 0.130 | OK | OK | OK | 430 CHF |
| B_desk | 0.82 | 0.135 | OK | OK | OK | 480 CHF |
| C_opt | 0.94 | 0.120 | OK | OK | OK | 900 CHF |
| D_full | 1.20 | 0.170 | FALL 45 | FALL | FALL | 1700 CHF |
| E_offboard | 0.80 | 0.130 | OK | OK | OK | 430 CHF |
| F_lowballast | 0.87 | 0.110 | OK | OK | OK | 470 CHF |

E = A. F tiefster COM der Steher. D tot. Walk als Naechstes nur A/B/C/E/F.

Gegenkontrolle Claude Code 2026-09-02: alle Zahlen reproduziert. Aber die
Spalten Seite und Hinten sind nicht aussagekraeftig — der Stoss greift in der
Schwerpunktachse an und kippt nichts. Es traegt nur die Ruhe-Spalte (und damit
das Urteil ueber D). Kippschwelle je Ente:
`python3 tests/tip_test.py --sweep`. Begruendung:
docs/reviews/2026-09-02-claude-tip-test.md
