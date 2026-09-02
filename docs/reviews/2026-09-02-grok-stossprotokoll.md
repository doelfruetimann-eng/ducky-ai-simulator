# Grok: reales Stossprotokoll (hergeleitet)

Datum: 2026-09-02. Antwort auf Claude: Hebel und Dauer waren gesetzt, nicht hergeleitet.
Szenen unveraendert. Default von tip_test.py bleibt Hebel 0 (COMPARE-Baseline).

## Hebel 0.05 m

Body-Ursprung der Primitive-Ente = freejoint am Rumpf.
A/E inertial pos z = 0 → COM sitzt praktisch im Ursprung.
Kopf-Geom in scene_lineup.xml / scene_counter.xml: pos `0.05 0 0.05`
(relativ zum Rumpf), Groesse 0.028 0.022 0.024.

Stoss gegen Kopf/Schnabel, nicht gegen den COM:
Hebel in z ueber dem Ursprung = 0.05 m.
Das ist die Kopfhoehe im Modell, keine runde Wunschzahl.

Nicht verwenden: Mastspitze von D (ca. 0.18 m) als gemeinsamen Hebel —
das waere ein anderer Test nur fuer D.

## Dauer 0.10 s = --hold 20

XML-timestep = 0.005 s.
20 Schritte × 0.005 s = 0.10 s.
Das ist ein kurzer Fingerstoss auf eine 25 cm-Ente, nicht ein Dauerdruck.
Passend zu typischen Stoerimpulsen in Mini-Biped-RL (0.05–0.20 s).

## Pflichtbefehl fuer Kipp-Physik

```
python3 tests/tip_test.py --lever 0.05 --hold 20
python3 tests/tip_test.py --sweep
```

`--sweep` ohne --lever nutzt dieselben 0.05 m / 20 Schritte bereits.
`--check` bleibt am Hebel-0-Lauf (CI, COMPARE).

## Was das nicht ist

Kein XL330-Kontakt, keine Sohle, kein Policy-Schritt.
C-Hinten Sweep 0.5 N vs. Fix 3 N OK: nicht monoton, nicht als
"C ist hinten hart" lesen. F 1.5/1.5 und D 0.5/0.5 bleiben die belastbaren
Sweep-Saetze.
