# Kosten der Modellvarianten (CH, ca. Sept. 2026)

Rundungspreise, inkl. typischer Shop-MwSt., ohne Arbeitszeit.
Microduck-Listenpreis 340 EUR; an der CH-Tuer eher 400-480 CHF.

| | A Stock | B Desk+ | C Opt | D Full |
|---|---|---|---|---|
| Im Sim | A_stock | B_desk | C_opt | D_full |
| Masse Sim | 0.80 kg | 0.82 kg | 0.94 kg | 1.20 kg |
| Steht mit Stock-Gang | ja | eher ja | testen | nein, hoher COM |
| Hardware neu | **430 CHF** | **480 CHF** | **900 CHF** | **1700 CHF** |

C nutzt den Mac mini M5 als Hirn (kein Jetson in der Summe).
Jetson auf die Ente: C eher 1200 CHF.

Test:
```bash
python -m mujoco.viewer --mjcf models/scene_lineup.xml
```
