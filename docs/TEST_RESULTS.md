# Simulator-Test 2026-09-02

Szene models/scene_lineup.xml, Skript tests/tip_test.py, MuJoCo 3.12.

| Ente | Masse | COM-Höhe | Ruhe | Seite | Hinten |
|---|---|---|---|---|---|
| A_stock | 0.80 kg | 0.130 m | OK 0.1 | OK | OK |
| B_desk | 0.82 kg | 0.135 m | OK | OK | OK |
| C_opt | 0.94 kg | 0.120 m | OK | OK | OK |
| D_full | 1.20 kg | 0.170 m | FALL 44.7 | FALL | FALL |

D fällt schon im Stand (X5-Mast). C ist schwerer als A, COM aber tiefer.
Kein Watschel-Test. Nächster Schritt: Walk-Policy nur auf A/B/C.
