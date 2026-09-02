# Ducky AI Simulator

Werkstatt für eine angepasste [Microduck](https://github.com/pollen-robotics/microduck)-Simulation (Pollen Robotics / Hugging Face).

**Maschine:** Mac mini M5 16 GB = Viewer + kleine KI. PC + RTX 4060 8 GB = Training. Hugging Face Jobs = Training ohne lokale GPU.

## Schnellstart (Mac mini)

```bash
git clone https://github.com/doelfruetimann-eng/ducky-ai-simulator.git
cd ducky-ai-simulator
pip install mujoco
python -m mujoco.viewer --mjcf models/scene_primitive.xml
```

## Links

- Upstream Runtime: https://github.com/pollen-robotics/microduck
- Training / MJCF: https://github.com/pollen-robotics/microduck_rl
- Browser-Sim: https://huggingface.co/spaces/pollen-robotics/microduck-simulator
- Älteres Notiz-Repo: https://github.com/doelfruetimann-eng/microduck-upgrade

STLs aus `microduck_rl` nicht committen (CC BY-NC-SA). Siehe `docs/`.
