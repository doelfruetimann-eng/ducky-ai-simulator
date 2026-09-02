#!/usr/bin/env python3
from pathlib import Path
import math
import mujoco

ROOT = Path(__file__).resolve().parents[1]
SCENE = ROOT / "models" / "scene_lineup.xml"
DUCKS = ["A_stock", "B_desk", "C_opt", "D_full"]

def body_id(model, name):
    return mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, name)

def tilt_deg(data, bid):
    z = data.xmat[bid].reshape(3, 3)[:, 2]
    c = max(-1.0, min(1.0, float(z[2])))
    return math.degrees(math.acos(c))

def settle(model, data, steps=800):
    for _ in range(steps):
        mujoco.mj_step(model, data)

def run_case(model, duck, kind):
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)
    bid = body_id(model, duck)
    if kind == "nudge_side":
        data.xfrc_applied[bid, 1] = 2.5
        mujoco.mj_step(model, data)
        data.xfrc_applied[bid] = 0
    elif kind == "nudge_back":
        data.xfrc_applied[bid, 0] = -3.0
        mujoco.mj_step(model, data)
        data.xfrc_applied[bid] = 0
    settle(model, data, 1200)
    t = tilt_deg(data, bid)
    z = float(data.xpos[bid][2])
    return t, z, t < 35 and z > 0.06

def main():
    model = mujoco.MjModel.from_xml_path(str(SCENE))
    print(f"{'duck':10} {'kg':>6} {'com_z':>7}  rest  side   back")
    for duck in DUCKS:
        bid = body_id(model, duck)
        mass = float(model.body_mass[bid])
        data = mujoco.MjData(model)
        mujoco.mj_forward(model, data)
        com_z = float(data.subtree_com[bid][2])
        rest_t, _, rest_ok = run_case(model, duck, "rest")
        side_t, _, side_ok = run_case(model, duck, "nudge_side")
        back_t, _, back_ok = run_case(model, duck, "nudge_back")
        def flag(ok, t):
            return f"{'OK':>4} {t:5.1f}deg" if ok else f"{'FALL':>4} {t:5.1f}deg"
        print(f"{duck:10} {mass:6.2f} {com_z:7.3f}  {flag(rest_ok, rest_t)}  {flag(side_ok, side_t)}  {flag(back_ok, back_t)}")

if __name__ == "__main__":
    main()
