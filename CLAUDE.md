# CLAUDE.md — TrojanHorseAreana

> Claude Code configuration for the `thebardchat/TrojanHorseAreana` repository.

---

## Project Overview

This repository holds the **Hazel Green Trojans Sports Complex — Phase 1 3D Model**, a parametric architectural visualization of the North Alabama Regional Athletic Complex. It includes CadQuery 3D models, matplotlib renders, and FreeCAD conversion tooling.

This project operates under the [ShaneTheBrain Constitution](https://github.com/thebardchat/constitution/blob/main/CONSTITUTION.md).

---

## Infrastructure

All `thebardchat` repositories run on the following local-first infrastructure:

| Component | Detail |
|-----------|--------|
| **Compute** | Raspberry Pi 5 (16 GB RAM) |
| **Chassis** | Pironman 5-MAX by Sunfounder (NVMe RAID) |
| **Storage** | 2x WD Blue SN5000 2 TB NVMe — RAID 1 via mdadm |
| **Core path** | `/mnt/shanebrain-raid/shanebrain-core/` |
| **Dev environment** | Claude Code on Pi 5 |

> Pi before cloud. Privacy before convenience. — Pillar 4

---

## Repository Structure

```
TrojanHorseAreana/
  build_3d_model.py               # CadQuery parametric 3D model generator
  render_floorplan.py             # matplotlib 2D floor plan renderer
  render_3d_views.py              # matplotlib 3D perspective view renderer
  import_to_freecad.py            # FreeCAD STEP conversion macro
  Hazel_Green_Trojans_Complex.step # Universal CAD exchange format
  Hazel_Green_Trojans_Complex.stl  # 3D print / mesh format
  render_floorplan_2d.png         # Annotated 2D floor plan
  render_aerial.png               # Bird's eye aerial view
  render_entrance.png             # Front entrance perspective
  render_arena.png                # Interior arena view
  README.md                       # Public-facing project documentation
  CLAUDE.md                       # This file — Claude Code project context
```

---

## Working With This Repo

- **Do not copy** the Constitution into other repos. Link to it instead.
- Reference line for other repos:
  ```md
  This project operates under the [ShaneTheBrain Constitution](https://github.com/thebardchat/constitution/blob/main/CONSTITUTION.md).
  ```
- Regenerate models with `python3 build_3d_model.py`, renders with `python3 render_floorplan.py` and `python3 render_3d_views.py`.
- Dependencies: `cadquery`, `matplotlib`, `Pillow`, `numpy`.

---

## Credits

Built with Claude (Anthropic) · Runs on Raspberry Pi 5 + Pironman 5-MAX

| Partner | Role |
|---------|------|
| **Claude by Anthropic** · [claude.ai](https://claude.ai) | Co-built this entire ecosystem |
| **Raspberry Pi 5** · [raspberrypi.com](https://www.raspberrypi.com) | Local compute backbone |
| **Pironman 5-MAX** · [pironman.com](https://www.pironman.com) | NVMe RAID 1 chassis that made it real |

---

*Created for Hazel Green Trojans — [@thebardchat](https://github.com/thebardchat) · Hazel Green, Alabama*

## Claude Code Rules
- Commit and push directly to `claude/trojans-sports-complex-3d-r07Pw`. Do NOT create branches.
- Run build/test commands before committing.
- Update CLAUDE.md session log before final commit.
