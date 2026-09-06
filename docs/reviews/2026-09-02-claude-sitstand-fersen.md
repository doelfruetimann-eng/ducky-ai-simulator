# Sitstand: Fersen-Flackern nach dem Aufstehen (Claude Code, 2026-09-02)

Doelfs Beobachtung auf dem Mac mini: Sit ok, Stand-up oszilliert an den
Fersen. Auflagen: kein CAD, keine neue Masse. Beides eingehalten - hier wurde
nur gemessen, im microduck_rl-Checkout, mit den offiziellen ONNX. Nichts an
Modellen, nichts an der BASELINE, nichts in diesem Repo ausser dieser Datei.

## Ergebnis in einem Satz

Nach dem Aufstehen steht die Sitstand-Policy vorne auf den Fuessen; die
rechte Ferse liegt an der Kontaktgrenze und macht/bricht den Bodenkontakt
etwa 29-mal pro Sekunde. Das ist das Flackern. Es ist eine Eigenschaft der
Stand-Haltung von `alpha_sitstand.onnx`, kein Simulator-Fehler - und es
verschwindet, sobald nach dem Aufstehen `alpha_stand.onnx` uebernimmt.

## Nachgestellt (Linux x86_64, MuJoCo 3.12.0, onnxruntime 1.29.0, ohne Viewer)

Ablauf: 3 s stehen (Flag 0) -> Flag 1 (sitzen) -> 6 s -> Flag 0 (aufstehen)
-> 13 s messen. 50 Hz, Timestep 0.005, Dezimation 4, wie `infer_policy.py`.
microduck_rl auf `5bbe963`. Fusskraefte je Fuss ueber `mj_contactForce`,
Ferse/Zehe getrennt nach Lage des Kontaktpunkts vor oder hinter dem Knoechel.

Sitzen funktioniert: Rumpf 59 mm, beide Fuesse am Boden. Aufstehen
funktioniert: Rumpf 116 mm nach 0.8 s, Fuesse tragen zusammen 7.5 N.

| Zustand (Fenster 12-22 s) | Ferse L | Ferse R | Zehe L / R | Ferse R ab/auf | Nick |
|---|---|---|---|---|---|
| Sitstand nach dem Aufstehen | 1.65 N | 0.60 N, min 0 | 1.54 / 3.44 N | **29 pro s** | +3.5 Grad |
| alpha_stand allein | 1.70 N | 1.89 N, min 1.6 | 1.91 / 1.73 N | 0 | +0.3 Grad |
| Aufstehen, dann nach 1 s alpha_stand | 1.69 N | 1.88 N, min 1.6 | 1.91 / 1.75 N | 0 | +0.3 Grad |
| Aufstehen, dann nach 3 s alpha_stand | 1.67 N | 1.88 N | 1.92 / 1.76 N | 0 | +0.3 Grad |

Lesart: alpha_stand verteilt die Last gleichmaessig auf Ferse und Zehe, Nick
praktisch null. Die Sitstand-Policy haelt nach dem Aufstehen 3.5 Grad Nick
und verlagert rechts fast alles auf die Zehe. Die rechte Ferse traegt dann
0.6 N mit Untergrenze 0 - sie hebt und setzt staendig. Der Knoechel selbst
bewegt sich dabei nur 2 Milliradiant; im Gelenk wackelt nichts, es flackert
der Kontakt an der Fersenkante.

## Was es NICHT ist (alle Varianten zeigen dasselbe Flackern)

| Variante | Ferse R ab/auf | Bemerkung |
|---|---|---|
| Motorstromgrenze 1.75 A = 0.64 Nm (bam) | gleich | Doelf lief ohne (`--current-limit 0`), macht keinen Unterschied |
| weiche Sohle `--foot-solref 0.04` | gleich | |
| Flag-Rampe 2 s statt Sprung | gleich | Training flippt den Flag ohnehin sprunghaft, nur das Belohnungsziel ist gerampt (`POSTURE_RAMP_S`) |
| Timestep 0.002 wie im XML | gleich | |
| Sitzdauer 2 s / 15 s | gleich | |
| Startstreuung, 5 Seeds | gleich | Aufstehen beruhigt in 0.76-0.94 s, dann Flackern |

Also nicht Stromgrenze, nicht Sohle, nicht Zeitschritt, nicht Uebergangsart,
nicht Zufall. Es ist die Haltung, die die Policy nach dem Aufstehen einnimmt.

Nebenbefund: eine Kraftschwankung von 0.2-0.3 N bei 9-13 Hz haben ALLE
Staender, auch alpha_stand allein. Das ist Kontaktzittern der Mesh-Sohle auf
der Ebene und unsichtbar - nur relevant, damit es niemand mit dem
Fersen-Flackern verwechselt.

## Was Doelf tun kann, ohne etwas zu aendern

Alle drei Policies laden und nach dem Aufstehen die Leertaste druecken:

```
mjpython scripts/infer_policy.py \
  --walking  ~/microduck_policies/alpha_walking.onnx \
  --standing ~/microduck_policies/alpha_stand.onnx \
  --sitstand ~/microduck_policies/alpha_sitstand.onnx \
  --new-cmd-obs --current-limit 0
```

Im Terminal: `Y` = sitzen, `Y` = aufstehen, dann etwa zwei Sekunden warten,
dann **Leertaste**. Die Leertaste setzt das Geschwindigkeitskommando auf null
und ruft `_update_policy_session()`; bei Betrag 0 wechselt das Skript auf
`alpha_stand` (`infer_policy.py`, `set_vel_cmd` und `_update_policy_session`).
Das Flackern hoert auf, weil alpha_stand die Fersen belastet.

Bedingung: `--walking` UND `--standing` muessen geladen sein.
`_update_policy_session` kehrt sonst sofort zurueck ("Only one policy
loaded, no switching") - mit nur `--standing --sitstand` tut die Leertaste
nichts. Das ist so im Skript, nicht von mir.

Warum das Skript nicht selbst umschaltet: `toggle_sit` laesst nach dem
Aufstehen absichtlich die Sitstand-Policy stehen ("it would take over
mid-rise from a seated state it wasn't trained on"). Nach 1 s war die
Uebergabe hier sauber (Tabelle oben), nach 0 s nicht getestet. Zwei
Sekunden warten ist die sichere Seite.

## Zwei Dinge, die ich nicht erklaeren kann

1. **Sitstand nur stehen, ohne je zu sitzen** (vom Start-qpos aus): Nick
   +31 Grad, beide Fersen 0 N, Rumpf 111 mm. Die Policy steht dann auf den
   Zehen, stark vorgeneigt, stabil. Vermutlich ist das Start-qpos des Skripts
   kein Zustand, aus dem sie trainiert wurde. Wer die Sitstand-Policy allein
   startet, sieht diese Haltung. Nicht weiter verfolgt.
2. **Mac gegen Linux**: hier ohne Viewer, x86_64, MuJoCo 3.12.0. Doelfs Mini
   hat arm64 und moeglicherweise eine andere MuJoCo-Version. Die Haltung
   (Nick +3.5, Ferse R fast unbelastet) ist eine Policy-Eigenschaft und sollte
   dort gleich sein; die exakte Flackerrate kann abweichen.

## Fehler von mir, festgehalten

Mein erster Treiber gab der Policy den rohen Beschleunigungssensor statt
der projizierten Schwerkraft (Konstruktor-Default `use_projected_gravity=False`,
das Skript setzt `True`). Damit stand die Policy nach dem Flag gar nicht
auf, und ich haette beinahe "Aufstehen kaputt" gemeldet. Nach der Korrektur
stimmt der Treiber mit dem Skript ueberein. Steht hier, damit die naechste
Engine den Fehler nicht wiederholt.

## Fuer Grok

Physik-Frage, nicht meine: Ist die vorneigende Stand-Haltung von
alpha_sitstand mit 0.6 N auf der rechten Ferse auf dem echten Roboter ein
Problem (Servo-Zittern, Verschleiss), oder nur ein Sim-Artefakt der harten
Mesh-Sohle? Auf der PU-Sohle mit mu 1.5-2.5 koennte es anders aussehen.
Gemessen mit `--foot-friction 2.0` (PU-Sohle nachgestellt): Ferse R 0.88 N, Untergrenze 0.00, ab/auf 28.1 pro s - Reibung aendert am Flackern nichts, es ist die Vertikallast, nicht der Grip.

## Anhang: der Treiber, zum Nachlaufen

Liegt nicht im Repo (Karte: nur ein Review). Braucht den microduck_rl-Checkout
daneben und die drei ONNX unter `~/microduck_policies/`. Aufruf:
`python3 sitstand_probe.py --label BASIS`, Varianten siehe `--help`.

```python
#!/usr/bin/env python3
"""Headless: sitstand-Policy stehen -> sitzen -> aufstehen, Fersen-Oszillation messen.
Nutzt PolicyInference aus microduck_rl/scripts/infer_policy.py unveraendert."""
import sys, argparse, math, numpy as np
sys.path.insert(0, "../microduck_rl/scripts")
import mujoco, mujoco.viewer  # noqa
from infer_policy import PolicyInference, MICRODUCK_XML

p = argparse.ArgumentParser()
p.add_argument("--torque-limit", type=float, default=None, help="Nm, wie --current-limit*kt (1.75 A -> 0.6405)")
p.add_argument("--foot-solref", type=float, default=None)
p.add_argument("--foot-friction", type=float, default=None)
p.add_argument("--ramp", type=float, default=0.0, help="s, Flag 1->0 linear statt Sprung")
p.add_argument("--timestep", type=float, default=0.005)
p.add_argument("--decimation", type=int, default=4)
p.add_argument("--kp-scale", type=float, default=1.0)
p.add_argument("--label", default="")
p.add_argument("--no-sit", action="store_true", help="sitstand-Policy nur stehen lassen")
p.add_argument("--sit-dur", type=float, default=6.0)
p.add_argument("--seed", type=int, default=None, help="kleine Startstreuung")
p.add_argument("--series", action="store_true", help="Zeitreihe 8.5-14 s drucken")
p.add_argument("--stand-only", action="store_true", help="nur alpha_stand, nie sitzen")
p.add_argument("--handover", type=float, default=None, help="s: nach dem Aufstehen an alpha_stand uebergeben")
a = p.parse_args()

import os; os.chdir("../microduck_rl")
model = mujoco.MjModel.from_xml_path(MICRODUCK_XML)
model.opt.timestep = a.timestep
data = mujoco.MjData(model)
if a.torque_limit:
    model.actuator_forcerange[:, 0] = -a.torque_limit; model.actuator_forcerange[:, 1] = a.torque_limit
    model.actuator_forcelimited[:] = 1
feet = [mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, n) for n in ("left_foot_collision", "right_foot_collision")]
for g in feet:
    if a.foot_solref: model.geom_solref[g, 0] = a.foot_solref; model.geom_solref[g, 1] = 1.0
    if a.foot_friction: model.geom_friction[g, 0] = a.foot_friction
if a.kp_scale != 1.0:
    model.actuator_gainprm[:, 0] *= a.kp_scale; model.actuator_biasprm[:, 1] *= a.kp_scale

STAND = "../microduck_policies/alpha_stand.onnx"
pol = PolicyInference(model, data, sitstand_onnx_path=None if a.stand_only else "../microduck_policies/alpha_sitstand.onnx",
                      standing_onnx_path=STAND if (a.stand_only or a.handover) else None, new_cmd_obs=True,
                      use_projected_gravity=True)  # wie das Skript (default: not --raw-accelerometer)
trunk = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "trunk_base")
if a.seed is not None:
    rng = np.random.default_rng(a.seed); data.qpos[7:] += rng.normal(0, 0.01, model.nq - 7); data.qvel[:2] = rng.normal(0, 0.02, 2)
    mujoco.mj_forward(model, data)
ank = [int(model.actuator_trnid[i, 0]) for i in (4, 13)]
ank_q = [int(model.jnt_qposadr[j]) for j in ank]; ank_v = [int(model.jnt_dofadr[j]) for j in ank]

ctrl_dt = a.timestep * a.decimation
T_SIT, T_STAND, T_END = 3.0, 3.0 + a.sit_dur, 3.0 + a.sit_dur + 13.0
rows = []
t = 0.0; ramp_start = None
f6 = np.zeros(6)
while t < T_END:
    if a.stand_only or a.no_sit: pass
    elif ramp_start is None and t >= T_SIT and pol.sit_mode is False and t < T_STAND: pol.toggle_sit()
    if a.handover and ramp_start is not None and t >= ramp_start + a.handover and pol.current_policy == "sit":
        pol.current_policy = "standing"; pol.ort_session = pol.standing_session; pol._update_command(); print(f"  -> handover an alpha_stand bei t={t:.1f}")
    if (not a.stand_only) and t >= T_STAND and pol.sit_mode:
        pol.toggle_sit(); ramp_start = t
    if a.ramp > 0 and ramp_start is not None:
        pol.command[0] = max(0.0, 1.0 - (t - ramp_start) / a.ramp)
    act = pol.infer(); pol.apply_action(act)
    for _ in range(a.decimation): mujoco.mj_step(model, data)
    # Fusskraefte und Ferse/Zehe: Kontaktpunkt relativ zum Knoechel entlang Rumpf-x
    fwd = data.xmat[trunk].reshape(3, 3)[:, 0]
    fn = [0.0, 0.0]; heel = [0.0, 0.0]; toe = [0.0, 0.0]
    for c in range(data.ncon):
        con = data.contact[c]
        for k, g in enumerate(feet):
            if con.geom1 == g or con.geom2 == g:
                mujoco.mj_contactForce(model, data, c, f6); f = abs(f6[0])
                fn[k] += f
                d = float(np.dot(con.pos - data.xanchor[ank[k]], fwd))
                (toe if d > 0 else heel)[k] += f
    R33 = data.xmat[trunk].reshape(3, 3); pitch = math.degrees(math.atan2(-R33[2, 0], math.hypot(R33[0, 0], R33[1, 0])))
    rows.append((t, float(data.xpos[trunk][2]), *[float(data.qpos[q]) for q in ank_q], *[float(data.qvel[v]) for v in ank_v], *fn, *heel, *toe, pitch))
    t += ctrl_dt

R = np.array(rows); tt = R[:, 0]
def win(lo, hi): return R[(tt >= lo) & (tt < hi)]
def freq(sig):
    sig = sig - sig.mean(); 
    if sig.std() < 1e-9: return 0.0
    sp = np.abs(np.fft.rfft(sig)); fr = np.fft.rfftfreq(len(sig), ctrl_dt); sp[0] = 0
    return float(fr[np.argmax(sp)])
S = win(2.0, 3.0); Q = win(T_STAND+3, T_END); U = win(T_STAND, T_STAND+3); Z = win(T_STAND-2, T_STAND)
zf = Q[:,1].mean(); settled = None
for i in range(len(R)):
    if tt[i] < T_STAND: continue
    W = R[(tt >= tt[i]) & (tt < tt[i]+1.0)]
    if len(W) >= 40 and abs(W[:,1]-zf).max() < 0.003 and (W[:,6] > 0.05).all() and (W[:,7] > 0.05).all() and np.ptp(W[:,12]) < 1.0:
        settled = tt[i] - T_STAND; break
print(f"  Aufstehen beruhigt nach {settled if settled is not None else float('nan'):.2f} s (Hoehe ±3 mm, beide Fuesse am Boden, Nick <1 Grad ueber 1 s)")
Uw = win(T_STAND, T_STAND+3); print(f"  Aufsteh-Phase: Nick p2p {np.ptp(Uw[:,12]):.1f} Grad, Ferse L Nulldurchgaenge {int((np.diff((Uw[:,8] > 0.05).astype(int)) != 0).sum())}, Ferse R {int((np.diff((Uw[:,9] > 0.05).astype(int)) != 0).sum())}, Fuss L abgehoben {(Uw[:,6] < 0.05).sum()} Schritte, R {(Uw[:,7] < 0.05).sum()}")
if a.series:
    print("     t    z_mm  nick_deg   L_ferse  L_zehe   R_ferse  R_zehe   ankL_deg ankR_deg")
    for r in R[(tt >= T_STAND-0.5) & (tt < T_STAND+5.0)][::5]:
        print(f"  {r[0]:5.1f}  {r[1]*1000:5.0f}  {r[12]:7.1f}   {r[8]:6.2f}  {r[10]:6.2f}   {r[9]:6.2f}  {r[11]:6.2f}   {math.degrees(r[2]):7.1f} {math.degrees(r[3]):7.1f}")
print(f"[{a.label}] ts={a.timestep} dec={a.decimation} torque={a.torque_limit} solref={a.foot_solref} mu={a.foot_friction} ramp={a.ramp} kp×{a.kp_scale}")
print(f"  Sitzen 7-9 s: trunk_z {Z[:,1].mean()*1000:.0f} mm, Fusskraft L/R {Z[:,6].mean():.2f}/{Z[:,7].mean():.2f} N, ohne Kontakt L {(Z[:,6]<0.05).sum()}/{len(Z)}")
print(f"  Sitz erreicht (t=8.9)? trunk_z={win(8.8,9.0)[:,1].mean()*1000:.0f} mm  |  Stand vorher {S[:,1].mean()*1000:.0f} mm  |  nach Aufstehen (12-22 s) {Q[:,1].mean()*1000:.0f} mm, std {Q[:,1].std()*1000:.2f} mm")
print(f"  Knoechel-Winkelgeschw. RMS  Stand vorher L/R {np.sqrt((S[:,4]**2).mean()):.3f}/{np.sqrt((S[:,5]**2).mean()):.3f}  |  nach Aufstehen {np.sqrt((Q[:,4]**2).mean()):.3f}/{np.sqrt((Q[:,5]**2).mean()):.3f} rad/s")
print(f"  Dominante Frequenz nach Aufstehen: trunk_z {freq(Q[:,1]):.1f} Hz, Knoechel L {freq(Q[:,4]):.1f} Hz")
print(f"  Fusskraft L: min {Q[:,6].min():.2f} max {Q[:,6].max():.2f} N (Schritte ohne Kontakt: {(Q[:,6]<0.05).sum()}/{len(Q)})   R: min {Q[:,7].min():.2f} max {Q[:,7].max():.2f} N (ohne: {(Q[:,7]<0.05).sum()})")
print(f"  Ferse/Zehe-Anteil L: {Q[:,8].mean():.2f}/{Q[:,10].mean():.2f} N   R: {Q[:,9].mean():.2f}/{Q[:,11].mean():.2f} N   (Stand vorher L {S[:,8].mean():.2f}/{S[:,10].mean():.2f})")
def osc(W, name):
    fl, fr = W[:,6], W[:,7]; dur = len(W) * ctrl_dt
    zc = lambda h: int((np.diff((h > 0.05).astype(int)) != 0).sum()) / dur
    print(f"  {name}: Ferse L {W[:,8].mean():.2f} N (min {W[:,8].min():.2f}, ab/auf {zc(W[:,8]):.1f}/s) | Ferse R {W[:,9].mean():.2f} N (min {W[:,9].min():.2f}, ab/auf {zc(W[:,9]):.1f}/s) | Zehe L/R {W[:,10].mean():.2f}/{W[:,11].mean():.2f} N | Nick {W[:,12].mean():+.1f} Grad | Knoechel L/R {math.degrees(W[:,2].mean()):+.1f}/{math.degrees(W[:,3].mean()):+.1f} Grad")
osc(S, "Stand vorher 2-3 s"); osc(Q, "nach Aufstehen 12-22 s"); osc(win(18.0, 22.0), "spaet 18-22 s")
print(f"  Aufsteh-Phase 9-12 s: trunk_z std {U[:,1].std()*1000:.1f} mm, Knoechel RMS {np.sqrt((U[:,4]**2).mean()):.3f} rad/s, Fuss L ohne Kontakt {(U[:,6]<0.05).sum()}/{len(U)}")
```
