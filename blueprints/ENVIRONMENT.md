# ENVIRONMENT — KEYSTONE

First-run check: 2026-10-03, ~4:59 PM CT (P1-T-000).

## Where KEYSTONE actually runs (differs from prompt §6)

- The prompt assumes a Windows desktop agent on **pulsar00100** with a clone at `C:\Users\Hubby\TrojanHorseAreana\`. **That is not how this session ran.**
- KEYSTONE runs on a **separate Linux box** (Debian GNU/Linux 13 "trixie", x86_64), not on pulsar00100. It has no access to Shane's Windows PC, and this session was told not to touch it.
- Working copy: `/workspace/TrojanHorseAreana` (cloned with `gh`, logged in as `thebardchat`). Branch: `grok/keystone`, cut from `main` at `8a2f4c6`.
- Shane's asset folder `C:\Users\Hubby\Desktop\ARENA\` was **not read directly**. Shane gave this box copies of its 4 files at `/workspace/arena_src/`. Sizes and times came from Shane. See ASSETS.md.
- **Bridge files:** KEYSTONE writes `blueprints/STATUS.json` + `blueprints/STATUS.md` and pushes them to `grok/keystone`. The plan is that KEYSTONE copies them to `C:\Users\Hubby\Desktop\ARENA\_KEYSTONE\` at session end. **That copy was not done in this bootstrap session, and `_KEYSTONE` was not created** (no pulsar00100 access). **The GitHub mirror is the reliable source.** `keystone_status.sh` already falls back to `raw.githubusercontent.com/.../grok/keystone/blueprints/STATUS.json` when pulsar is unreachable.
- **Daily 6:00 AM CT scheduled run:** not set up in this session. The Pi flags a stale STATUS file on its own after 26 h.
- Git identity for KEYSTONE commits (local to this clone only): `KEYSTONE (Grok Bot for thebardchat)` / thebardchat's GitHub noreply address.

## First-run check results

| Check (prompt §6, Linux equivalents) | Result |
|---|---|
| `python3 --version` | `Python 3.13.5` |
| `pip --version` | `pip 25.1.1 from /usr/lib/python3/dist-packages/pip (python 3.13)` (system pip; the system Python is externally managed, so installs go in a venv) |
| `git --version` | `git version 2.47.3` |
| `git remote -v` | `origin https://github.com/thebardchat/TrojanHorseAreana.git (fetch)` / `(push)` |
| `which freecad` | **not found** (exit 1). `freecadcmd` / `FreeCAD` also not found. FreeCAD isn't needed for 2D sheets |
| `gh --version` | `gh version 2.46.0`, logged in as `thebardchat` (repo scope) |
| `pdftotext` | `/usr/bin/pdftotext` (poppler-utils), used by validate.py for the stamp check |

## Python packages

Venv: `/workspace/.venv-keystone` (outside the repo, so nothing gets committed by accident).
Run tools with `/workspace/.venv-keystone/bin/python`. The system `python3` has no pyyaml.

| Package | Result |
|---|---|
| ezdxf | installed, 1.4.4 |
| matplotlib | installed, 3.11.2 |
| numpy | installed, 2.5.3 |
| pillow | installed, 12.3.0 |
| pyyaml | installed, 6.0.3 |
| cadquery | **installed, 2.8.0** (cadquery-ocp 7.9.3.1.1). Smoke test passed: a 1×2×3 box gave volume 6.0 |

Validate command (from repo root): `/workspace/.venv-keystone/bin/python blueprints/shared/validate.py`

## Asset locations

| Asset | Location | Status |
|---|---|---|
| Shane's ARENA folder | `C:\Users\Hubby\Desktop\ARENA\` (pulsar00100). Box copies at `/workspace/arena_src/` | 4 files, inventoried in ASSETS.md |
| Repo diorama | `hazel-green-complex-3d.html` (repo root, commit 8a2f4c6) | Protected, read-only |
| Grok-session proposal page with `/model.html` maquette | **UNKNOWN.** No `model.html` anywhere on this box's filesystem (searched 2026-10-03). The Grok share transcript on this box (`/workspace/trojan-horse-arena/grok-share.md`) only gives it as a web route (`/model.html`, `/model.html?zone=boys`, kiosk `http://YOUR-ADDRESS/model.html`). pulsar00100 was not searched | Ask Shane where it's hosted/saved |
| Phase 2 master floor plan image (55,000 SF, color-coded) | **Not in the ARENA folder.** Path unknown | Needed from Shane |
| Google Drive trailers ("Trojan Horse Arena Trailer v2 - Widescreen.m4v", "- Vertical.m4v") | Google Drive, per intake | Not inspected |
