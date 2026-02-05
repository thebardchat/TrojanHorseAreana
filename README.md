# Hazel Green Trojans Sports Complex — Phase 1 3D Model

**North Alabama Regional Athletic Complex**
*"Building Champions, One Mat at a Time"*

School Colors: **Red (#CC0000)** and **Black (#1A1A1A)**

---

## Phase 1 Specifications

| Attribute | Value |
|---|---|
| Building Footprint | 120 ft x 250 ft |
| Total Area | ~30,000 SF |
| Ceiling Height | 24 ft (single story, arena clearance) |
| Seating Capacity | ~800 (bleachers on 2 sides) |
| Wrestling Mats | 4 practice (32 ft dia.) + 1 championship (42 ft dia.) |
| Estimated Budget | $4M - $6M |

### Layout Zones

- **Entrance Lobby** (1,500 SF) — Public entry with ticket/check-in
- **Boys Locker Room** (2,000 SF)
- **Girls Locker Room** (2,000 SF)
- **S&C / Weight Room** (3,000 SF)
- **Restrooms & Concessions** (1,000 SF)
- **Wrestling Arena** — Championship center mat + 4 practice mats with bleacher seating

---

## Generated Files

### 3D CAD Models
- `Hazel_Green_Trojans_Complex.step` — Universal CAD exchange format (opens in any CAD software)
- `Hazel_Green_Trojans_Complex.stl` — 3D print / mesh render format

### Rendered Views
- `render_floorplan_2d.png` — Professional annotated 2D floor plan (for presentations)
- `render_aerial.png` — Bird's eye 3D aerial view
- `render_entrance.png` — Front entrance perspective
- `render_arena.png` — Interior arena view showing championship mat

### Source Scripts
- `build_3d_model.py` — CadQuery parametric 3D model generator (produces STEP & STL)
- `render_floorplan.py` — matplotlib 2D floor plan renderer
- `render_3d_views.py` — matplotlib 3D perspective view renderer

---

## How to Regenerate

```bash
# Install dependencies
pip install cadquery matplotlib Pillow numpy

# Generate 3D model (STEP + STL)
python3 build_3d_model.py

# Generate 2D floor plan
python3 render_floorplan.py

# Generate 3D rendered views
python3 render_3d_views.py
```

---

*Created for Hazel Green Trojans — SRM Dispatch Solutions*
