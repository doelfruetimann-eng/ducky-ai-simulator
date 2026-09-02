# Gegenkontrolle tip_test A-F (Claude Code, 2026-09-02)

Auftrag aus docs/ENGINEERS.md: wer eine Variante vorschlaegt, schreibt nicht
allein "bestanden". Grok hat E/F vorgeschlagen und gemessen, hier der zweite
Lauf. MuJoCo 3.12.0, Linux-Checkout, `python3 tests/tip_test.py`.

## 1. Zahlen bestaetigt

Alle sechs Werte aus docs/COMPARE.md reproduziert, Ziffer fuer Ziffer:
A 0.80/0.130, B 0.82/0.135, C 0.94/0.120, D 1.20/0.170, E 0.80/0.130,
F 0.87/0.110. D_full faellt im Stand bei 44.7 Grad. E steht wie A. F hat mit
0.110 m den tiefsten COM. **Nichts an COMPARE.md geaendert.**

## 2. Befund: die Spalten Seite und Hinten messen nichts

Der Stoss griff im Koerperursprung an, also praktisch in der Schwerpunktachse.
Eine Kraft durch den Schwerpunkt schiebt, sie kippt nicht — es gibt keinen
Hebelarm.

Gemessen an A_stock, 2.5 N seitlich:

| Stoss haelt | v_max | Neigung | Versatz |
|---|---|---|---|
| 1 Schritt (0.01 s) | 0.016 m/s | 0.1 Grad | 1.9 mm |
| 20 Schritte (0.10 s) | 0.313 m/s | 0.1 Grad | 24 mm |
| 400 Schritte (2.00 s) | 0.375 m/s | 0.1 Grad | 27 mm |

Auch zwei Sekunden Dauerkraft kippen die Ente nicht. Darum steht in COMPARE.md
bei allen fuenf Stehern dreimal OK: nicht weil sie stossfest sind, sondern weil
der Test nicht stossen kann. Die einzige echte Messung in der Tabelle ist die
Ruhe-Spalte — und die traegt das Urteil ueber D_full, das damit steht.

## 3. Mit Hebelarm kippt alles

`--lever 0.05 --hold 20` setzt dieselbe Kraft 5 cm ueber der Koerpermitte an:
bei 2.5 N liegen A, B, E, F auf der Seite (81-109 Grad). Ein fester Stoss ist
also entweder zu schwach (alle stehen) oder zu hart (alle liegen). Er trennt
die Enten nicht.

## 4. Vorschlag: Kippschwelle statt fester Stoss

`python3 tests/tip_test.py --sweep` sucht je Ente die kleinste Kraft, die sie
umlegt. Das trennt:

| Modell | Seite | Hinten |
|---|---|---|
| A_stock | 1.5 N | 0.5 N |
| B_desk | 1.5 N | 1.0 N |
| C_opt | 2.0 N | 0.5 N |
| D_full | 0.5 N | 0.5 N |
| E_offboard | 1.5 N | 0.5 N |
| F_lowballast | 1.5 N | 1.5 N |

Zwei Dinge, die die alte Tabelle verdeckt:

- **D_full ist auch hier Letzter, in beiden Richtungen.** Das Urteil "D tot"
  haelt unter dem schaerferen Test. Unabhaengig bestaetigt.
- **Die fuenf Steher sind nicht gleich.** F_lowballast haelt nach hinten das
  Dreifache von A/C/E aus, C_opt seitlich am meisten. Tiefster COM (F) und
  bester Seitenwert (C) fallen auseinander — COM-Hoehe allein sagt die
  Kippfestigkeit nicht voraus.

Die Zahlen sind ein Vorschlag, kein Urteil. Kraftniveau, Hebelhoehe (0.05 m)
und Stossdauer (0.10 s) sind gesetzt, nicht hergeleitet. Wer sie ersetzt,
misst neu.

## 5. Frage an die Runde (LOOP.md Umlauf 1)

Soll `--sweep` der neue Standard fuer COMPARE.md werden? Dann braucht es einen
begruendeten Hebel und eine begruendete Stossdauer — sonst tauschen wir eine
willkuerliche Zahl gegen die naechste. Bis das entschieden ist, bleibt der alte
Stoss der Standard und die Tabelle unveraendert.

Codex: bitte `--sweep` gegenlaufen. Grok: Hebelhoehe und Kraftniveau pruefen.

## 6. Was am Skript geaendert wurde

- A-F laufen in einem Lauf aus beiden Szenen; bisher A-D fest verdrahtet und
  E/F von Hand dazugerechnet.
- `--markdown` druckt die COMPARE-Tabelle, damit die Zahlen dort nicht mehr
  abgetippt werden.
- `--check` prueft gegen BASELINE im Skript. Exit 1 nur bei Abweichung vom
  gemessenen Stand — D_full faellt dort als erwartet eingetragen. Ein normaler
  Lauf endet mit Exit 0. Vorher gab D_full Exit 1, was tip_test.py in CI
  (docs/GIT.md) als Dauerrot gezeigt haette.
- `--lever` / `--hold` / `--sweep` neu. Standardverhalten unveraendert.
- Keine Szene angefasst, A-F vollstaendig.

## 7. Nachtrag: CI (Bedingung 2 aus docs/GIT.md)

`.github/workflows/tip-test.yml` laeuft bei Push und PR auf develop/main:
MuJoCo 3.12.0 aus `tests/requirements.txt`, dann `tests/tip_test.py --check`.
Gruen seit Lauf 2 auf develop (f9aa5d6). Lauf 1 war rot — `cache: pip` ohne
Dependency-Datei bricht setup-python ab; das Protokoll steht im Commit. Die Markdown-Tabelle landet in
der Job-Zusammenfassung, damit man die Zahlen im Lauf sieht, ohne Logs zu
oeffnen.

Die BASELINE haelt neu auch Masse und COM-Hoehe fest, nicht nur OK/FALL.
Grund: ein Urteil kippt nicht bei jeder Massenaenderung, eine still
geschoenrechnete Masse waere sonst gruen durchgelaufen — gegen "Do not hide
D_full mass" (CLAUDE.md) und "Masse nicht schoenrechnen" (ENGINEERS.md).
Toleranz 0.005 kg und 0.002 m.

Drei Faelle nachgestellt, alle brechen den Lauf mit Exit 1:

| Eingriff | Meldung |
|---|---|
| D_full still 1.20 -> 1.00 kg | `D_full: Masse 1.20 -> 1.00 kg` |
| F_lowballast aus der Szene geloescht | `Body 'F_lowballast' nicht in der Szene.` |
| Teillauf mit `--ducks A_stock` | `B_desk: fehlt im Lauf` (usw.) |

Damit ist "A-F nicht loeschen" nicht mehr nur eine Abmachung, sondern bricht
den Build. Wer eine Zahl bewusst aendert, aendert BASELINE mit und begruendet
es im Commit — das ist der Zweck, nicht eine Sperre.
