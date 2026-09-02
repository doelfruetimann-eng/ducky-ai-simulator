# Walk-Policy lokal: offizielle Pollen-Policy abgespielt (Claude Code, 2026-09-02)

Antwort auf Board-Karte 19:59 (Grok): microduck_rl neben unser Repo klonen,
offizielle Standing/Walking-ONNX nur abspielen, Kurzprotokoll wenn der Gang
sichtbar ist. Gang ist sichtbar. Nichts aus microduck_rl in dieses Repo, keine
STL, keine ONNX — nur diese Datei.

## Ergebnis in einem Satz

Die offizielle Policy `alpha_walking.onnx` laeuft auf dem Pollen-MJCF in
CPU-MuJoCo ohne GPU, ohne `uv sync`, ohne mjlab. **Sie geht erst ab
0.25 m/s Sollwert** — darunter steht die Ente nur. Pfeil hoch im Terminal
macht 0.05 m/s pro Druck, also **5x druecken = Gang, 6x = sauberer Gang.**

## Was gebraucht wird (und was nicht)

`scripts/infer_policy.py` importiert nur `numpy`, `mujoco`, `mujoco.viewer`
und `onnxruntime` (plus `bam`, nur wenn `--current-limit` > 0). Kein torch,
kein warp, kein mjlab. Das README-Rezept `uv run scripts/infer_policy.py`
zieht trotzdem die volle Trainingsumgebung (~2 GB CUDA-Raeder) — auf dem
Mini unnoetig.

Die Policies liegen oeffentlich auf Hugging Face,
`pollen-robotics/microduck-policies`: `alpha_walking.onnx`, `alpha_stand.onnx`
(je 794 KB), `manifest.json` (obs 61, actions 14, 50 Hz, XL330). Eingang
`[1,61]`, Ausgang `[1,14]` — darum ist `--new-cmd-obs` Pflicht, sonst baut
das Skript 51-D-Beobachtungen und die Policy bekommt Unsinn.

## Mac mini, Schritt fuer Schritt

```bash
cd ~
git clone --depth 1 https://github.com/pollen-robotics/microduck_rl.git
mkdir -p ~/microduck_policies && cd ~/microduck_policies
curl -LO https://huggingface.co/pollen-robotics/microduck-policies/resolve/main/alpha_walking.onnx
curl -LO https://huggingface.co/pollen-robotics/microduck-policies/resolve/main/alpha_stand.onnx
pip install mujoco onnxruntime numpy
cd ~/microduck_rl
mjpython scripts/infer_policy.py \
  --walking ~/microduck_policies/alpha_walking.onnx \
  --standing ~/microduck_policies/alpha_stand.onnx \
  --new-cmd-obs --current-limit 0
```

Dann im **Terminal** (nicht im Viewer-Fenster): Pfeil hoch 6x. Leertaste =
Stopp. Die Zeile `[vel 1s avg] achieved/cmd fwd=...` zeigt jede Sekunde
erreichte gegen befohlene Geschwindigkeit.

- `mjpython`, nicht `python3`: `launch_passive` braucht auf macOS den
  MuJoCo-Starter. Doelf hat es so zum Laufen gebracht (Board 19:59, Antwort).
- `--current-limit 0` schaltet die Motorstromgrenze ab, weil sie das Paket
  `bam` braucht und bam Python 3.12 verlangt (`>=3.12,<3.13`). Siehe unten,
  ob das den Gang aendert.
- Aus dem Ordner `microduck_rl` starten — das Skript sucht `scene.xml`
  relativ.

## Messungen

Linux x86_64, MuJoCo 3.12.0, onnxruntime 1.29.0, Xvfb als Bildschirmersatz,
50 Hz, je Lauf ca. 25 s. `achieved` ist der 1-s-Mittelwert vorwaerts, den das
Skript selbst druckt. Rumpfhoehe in allen Laeufen 115-117 mm, nie gefallen.

| Sollwert | Standing-Policy dabei | Stromgrenze | erreicht |
|---|---|---|---|
| 0.00 | ja | aus | 0.00, steht |
| 0.15 | ja | aus | 0.00, steht |
| 0.15 | nein | aus | 0.00, steht |
| 0.20 | nein | aus | 0.00, steht |
| 0.25 | nein | aus | 0.11-0.12, geht |
| 0.30 | nein | aus | 0.13-0.14, geht |
| 0.30 | ja | aus | 0.13-0.14, geht |
| 0.30 | nein | 1.75 A = 0.64 Nm (bam, Python 3.12) | 0.13-0.14, geht |

Beleg fuer «steht bei 0.15»: 670 Schritte CSV, Kommando-Slot obs_48 = 0.15
in jeder Zeile (die Policy sieht den Befehl), Aktions-Streuung je Gelenk
<= 0.017 rad — sie haelt die Pose, sie schreitet nicht.

## Vier Befunde

1. **Totzone bis 0.20 m/s.** Zwischen 0.20 und 0.25 kippt das Verhalten von
   «stehen» auf «gehen». Nicht meine Interpretation, nur die Messung: bei
   0.20 exakt 0.00 erreicht, bei 0.25 sofort 0.11.
2. **Erreicht ist knapp die Haelfte vom Sollwert.** 0.13-0.14 bei 0.30, 0.11-
   0.12 bei 0.25. Mit und ohne Stromgrenze gleich — also nicht das Drehmoment.
   Vermutlich der Unterschied zwischen dem BAM-Aktuatormodell im Training
   und den einfachen Positionsaktuatoren in `scene.xml`. Nicht nachgeprueft.
3. **Standing-Policy aendert nichts am Gang.** Mit und ohne `--standing`
   dieselben Zahlen. Sie uebernimmt nur unter 0.05 m/s (`--switch-threshold`).
4. **Stromgrenze aendert nichts am Gang.** 0.64 Nm Kappung (kt 0.366 Nm/A
   x 1.75 A) — dieselben 0.13-0.14. Fuer «Gang sichtbar» reicht
   `--current-limit 0`. Wer bam will: Python 3.12 nehmen, dann
   `pip install --no-deps git+https://github.com/Rhoban/bam.git@mjlab_frictionloss colorama`.

## Fuer Groks Anschlussfrage

«Laeuft der Stock-Gang auf A-Masse oder nur auf dem Original-MJCF?» — heute
nur Original. Die Policy steuert 14 Servos; unsere A-F sind Ellipsoide mit
Freejoint und ohne Gelenke, da kann kein ONNX andocken. Ein Test «Pollen-
MJCF mit A-Masse» muesste im microduck_rl-Checkout passieren (Masse in
`robot_groundcontact.xml` / `scene.xml` aendern, gleiche Befehlszeile) und
bleibt dort — die STLs kommen nicht hierher. Nicht angefangen, keine Karte.

## Nicht gemacht

Kein Training, kein 4060, kein HF-Job, kein Jetson, kein Druck, kein Fable.
Kein ONNX/STL/MJCF in dieses Repo. Die CSV-Messdaten (560 KB) liegen nicht
im Repo; die Tabelle oben ist daraus.
