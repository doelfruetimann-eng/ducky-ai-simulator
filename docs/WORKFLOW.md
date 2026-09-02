# Wie wir mit dem Simulator arbeiten

## Drei Ebenen

1. Hugging Face Space — Original-Ente im Browser.
2. `models/scene_primitive.xml` — unser Kit ohne STLs (Mac mini).
3. `microduck_rl` + RTX 4060 oder `--hf-jobs` — Training.

## Wer macht was

- Grok: XML, Masse, NFC-Szenen, Doku in diesem Repo.
- Du auf dem Mac mini: Viewer öffnen, steht/kippt sagen.
- Du auf der 4060 oder HF Jobs: Walk-Policy nur wenn die Opt-Ente taumelt.

## Mac mini M5 16 GB

```bash
pip install mujoco
python -m mujoco.viewer --mjcf models/scene_primitive.xml
```

Kein mjlab-Warp-Training auf dem Mini.

## PC RTX 4060 8 GB

```bash
git clone https://github.com/pollen-robotics/microduck_rl.git
cd microduck_rl
uv run train Mjlab-Velocity-Flat-MicroDuck --env.scene.num-envs 1024
```

OOM → 512 Envs. VRAM frei → 2048.

## Hugging Face

```bash
hf auth login
uv run train Mjlab-Velocity-Flat-MicroDuck --env.scene.num-envs 4096 --hf-jobs
```
