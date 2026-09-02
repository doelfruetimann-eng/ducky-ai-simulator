#!/usr/bin/env python3
"""Kipp-Test A-F. Eine Szene oder alle.

  python3 tests/tip_test.py                 # A-F aus beiden Szenen
  python3 tests/tip_test.py --markdown      # Tabelle fuer docs/COMPARE.md
  python3 tests/tip_test.py --check         # gegen BASELINE, Exit 1 bei Abweichung
  python3 tests/tip_test.py --scene models/scene_lineup.xml
  python3 tests/tip_test.py --ducks D_full F_lowballast
  python3 tests/tip_test.py --lever 0.05 --hold 20   # Stoss MIT Hebelarm

Der Standard-Stoss greift im Koerperursprung an, also praktisch in der
Schwerpunktachse: er schiebt, er kippt nicht (siehe
docs/reviews/2026-09-02-claude-tip-test.md). Die Zahlen bleiben so, wie sie in
docs/COMPARE.md stehen. Wer den echten Kipp-Stoss will, nimmt --lever.
"""
from pathlib import Path
import argparse
import math
import sys

import mujoco
import numpy as np

ROOT = Path(__file__).resolve().parents[1]

# Reihenfolge = Reihenfolge in docs/COMPARE.md. A-D und E/F stehen bewusst in
# getrennten Szenen (models/counter/README.md); hier laufen sie im selben Lauf.
LINEUP = ROOT / "models" / "scene_lineup.xml"
COUNTER = ROOT / "models" / "counter" / "scene_counter.xml"
SCENES = [
    (LINEUP, ["A_stock", "B_desk", "C_opt", "D_full"]),
    (COUNTER, ["E_offboard", "F_lowballast"]),
]

SETTLE_STEPS = 1200
SIDE_N = 2.5
BACK_N = 3.0
TILT_LIMIT_DEG = 35.0
HEIGHT_LIMIT_M = 0.06

# Gemessener Stand, den --check verteidigt: kg, COM z, dann Ruhe/Seite/Hinten.
# D_full FAELLT hier absichtlich und wiegt absichtlich 1.20 kg - das ist das
# Ergebnis, kein Skriptfehler. Masse und COM stehen mit drin, damit eine still
# geaenderte Masse auffaellt, auch wenn das Urteil gleich bleibt
# ("Do not hide D_full mass", CLAUDE.md; "Masse nicht schoenrechnen",
# docs/ENGINEERS.md). Wer eine Zahl bewusst aendert, aendert sie hier mit und
# begruendet das im Commit.
BASELINE = {
    "A_stock": (0.80, 0.130, True, True, True),
    "B_desk": (0.82, 0.135, True, True, True),
    "C_opt": (0.94, 0.120, True, True, True),
    "D_full": (1.20, 0.170, False, False, False),
    "E_offboard": (0.80, 0.130, True, True, True),
    "F_lowballast": (0.87, 0.110, True, True, True),
}
MASS_TOL_KG = 0.005
COM_TOL_M = 0.002


def body_id(model, name):
    bid = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, name)
    if bid < 0:
        raise SystemExit(f"Body '{name}' nicht in der Szene.")
    return bid


def tilt_deg(data, bid):
    z = data.xmat[bid].reshape(3, 3)[:, 2]
    c = max(-1.0, min(1.0, float(z[2])))
    return math.degrees(math.acos(c))


def settle(model, data, steps=SETTLE_STEPS):
    for _ in range(steps):
        mujoco.mj_step(model, data)


def run_case(model, duck, kind, steps=SETTLE_STEPS, lever=0.0, hold=1,
             force=None):
    """Ein Stoss, dann auslaufen lassen.

    lever = 0.0: Kraft im Koerperursprung (Stand COMPARE.md, kippt nicht).
    lever > 0.0: Kraft lever Meter darueber, echtes Kippmoment.
    force: ueberschreibt SIDE_N / BACK_N (fuer den Schwellen-Sweep).
    """
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)
    bid = body_id(model, duck)
    axis, newtons = {
        "rest": (None, 0.0),
        "nudge_side": (1, SIDE_N if force is None else force),
        "nudge_back": (0, -(BACK_N if force is None else force)),
    }[kind]
    if axis is not None:
        if lever > 0.0:
            force = np.zeros(3)
            force[axis] = newtons
            torque = np.zeros(3)
            for _ in range(hold):
                data.qfrc_applied[:] = 0
                point = np.array(data.xpos[bid], dtype=float)
                point[2] += lever
                mujoco.mj_applyFT(model, data, force, torque, point, bid,
                                  data.qfrc_applied)
                mujoco.mj_step(model, data)
            data.qfrc_applied[:] = 0
        else:
            for _ in range(hold):
                data.xfrc_applied[bid, axis] = newtons
                mujoco.mj_step(model, data)
            data.xfrc_applied[bid] = 0
    settle(model, data, steps)
    t = tilt_deg(data, bid)
    z = float(data.xpos[bid][2])
    return t, z, t < TILT_LIMIT_DEG and z > HEIGHT_LIMIT_M


def measure(scene, ducks, steps=SETTLE_STEPS, lever=0.0, hold=1):
    """Ein Modell laden, alle Enten daraus messen. Gibt Zeilen-Dicts zurueck."""
    model = mujoco.MjModel.from_xml_path(str(scene))
    rows = []
    for duck in ducks:
        bid = body_id(model, duck)
        data = mujoco.MjData(model)
        mujoco.mj_forward(model, data)
        row = {
            "duck": duck,
            "scene": scene.relative_to(ROOT).as_posix(),
            "mass": float(model.body_mass[bid]),
            "com_z": float(data.subtree_com[bid][2]),
        }
        for kind, key in (("rest", "rest"), ("nudge_side", "side"), ("nudge_back", "back")):
            t, _, ok = run_case(model, duck, kind, steps, lever, hold)
            row[key] = ok
            row[key + "_deg"] = t
        rows.append(row)
    return rows


def collect(scene_filter=None, duck_filter=None, steps=SETTLE_STEPS,
            lever=0.0, hold=1):
    rows = []
    for scene, ducks in SCENES:
        if scene_filter and scene.resolve() != scene_filter.resolve():
            continue
        if duck_filter:
            ducks = [d for d in ducks if d in duck_filter]
        if ducks:
            rows.extend(measure(scene, ducks, steps, lever, hold))
    if not rows:
        raise SystemExit("Keine Ente ausgewaehlt.")
    return rows


def print_table(rows):
    print(f"{'duck':14} {'kg':>6} {'com_z':>7}  rest  side   back")
    for r in rows:
        def flag(key):
            label = "OK" if r[key] else "FALL"
            return f"{label:>4} {r[key + '_deg']:5.1f}deg"
        print(f"{r['duck']:14} {r['mass']:6.2f} {r['com_z']:7.3f}  "
              f"{flag('rest')}  {flag('side')}  {flag('back')}")


def print_markdown(rows):
    print("| Modell | kg | COM z | Ruhe | Seite | Hinten |")
    print("|---|---|---|---|---|---|")
    for r in rows:
        def cell(key):
            return "OK" if r[key] else f"FALL {r[key + '_deg']:.0f}"
        print(f"| {r['duck']} | {r['mass']:.2f} | {r['com_z']:.3f} | "
              f"{cell('rest')} | {cell('side')} | {cell('back')} |")


SWEEP_N = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 7.0, 10.0, 15.0]


def sweep(scene_filter=None, duck_filter=None, lever=0.05, hold=20):
    """Kleinste Kraft, bei der die Ente kippt. Diskriminiert, anders als ein
    fester Stoss, bei dem entweder alle stehen oder alle liegen."""
    print(f"Kippschwelle, Hebel {lever:.3f} m, Stoss {hold * 0.005:.2f} s")
    print(f"{'duck':14} {'Seite':>8} {'Hinten':>8}")
    for scene, ducks in SCENES:
        if scene_filter and scene.resolve() != scene_filter.resolve():
            continue
        picked = [d for d in ducks if not duck_filter or d in duck_filter]
        if not picked:
            continue
        model = mujoco.MjModel.from_xml_path(str(scene))
        for duck in picked:
            cells = []
            for kind in ("nudge_side", "nudge_back"):
                hit = None
                for newtons in SWEEP_N:
                    _, _, ok = run_case(model, duck, kind, SETTLE_STEPS, lever,
                                        hold, newtons)
                    if not ok:
                        hit = newtons
                        break
                cells.append(f">{SWEEP_N[-1]:.0f} N" if hit is None else f"{hit:4.1f} N")
            print(f"{duck:14} {cells[0]:>8} {cells[1]:>8}")


def check(rows):
    """Vergleich gegen BASELINE. Gibt die Zahl der Abweichungen zurueck."""
    bad = 0
    seen = set()
    for r in rows:
        want = BASELINE.get(r["duck"])
        if want is None:
            print(f"{r['duck']}: kein Baseline-Eintrag")
            bad += 1
            continue
        seen.add(r["duck"])
        want_mass, want_com, *want_flags = want
        diffs = []
        if abs(r["mass"] - want_mass) > MASS_TOL_KG:
            diffs.append(f"Masse {want_mass:.2f} -> {r['mass']:.2f} kg")
        if abs(r["com_z"] - want_com) > COM_TOL_M:
            diffs.append(f"COM z {want_com:.3f} -> {r['com_z']:.3f} m")
        got_flags = [r["rest"], r["side"], r["back"]]
        for name, w, g in zip(("Ruhe", "Seite", "Hinten"), want_flags, got_flags):
            if w != g:
                diffs.append(f"{name}: {'OK' if w else 'FALL'} -> {'OK' if g else 'FALL'}")
        if diffs:
            print(f"{r['duck']}: " + ", ".join(diffs))
            bad += 1
    for duck in BASELINE:
        if duck not in seen:
            print(f"{duck}: fehlt im Lauf")
            bad += 1
    print("BASELINE gehalten." if not bad else f"{bad} Abweichung(en).")
    return bad


def main(argv=None):
    p = argparse.ArgumentParser(description="Kipp-Test A-F")
    p.add_argument("--scene", type=Path, help="nur diese Szene messen")
    p.add_argument("--ducks", nargs="+", help="nur diese Bodies messen")
    p.add_argument("--steps", type=int, default=SETTLE_STEPS, help="Schritte je Fall")
    p.add_argument("--lever", type=float, default=0.0,
                   help="Stoss so viele Meter ueber dem Koerperursprung")
    p.add_argument("--hold", type=int, default=1, help="Schritte, die der Stoss anliegt")
    p.add_argument("--markdown", action="store_true", help="Tabelle fuer COMPARE.md")
    p.add_argument("--check", action="store_true", help="gegen BASELINE pruefen (CI)")
    p.add_argument("--sweep", action="store_true",
                   help="Kippschwelle je Ente statt fester Stoss")
    args = p.parse_args(argv)

    if args.sweep:
        sweep(args.scene, args.ducks, args.lever or 0.05,
              args.hold if args.hold != 1 else 20)
        return 0

    rows = collect(args.scene, args.ducks, args.steps, args.lever, args.hold)
    if args.markdown:
        print_markdown(rows)
    else:
        print_table(rows)
    if args.check:
        if args.lever or args.hold != 1:
            print("--check gilt nur fuer den Standard-Stoss.")
            return 2
        return 1 if check(rows) else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
