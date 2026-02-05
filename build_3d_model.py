#!/usr/bin/env python3
"""
Hazel Green Trojans Sports Complex — Phase 1 3D Architectural Model
CadQuery-based parametric model generator.

Building: 120ft x 250ft rectangular, 24ft tall, single story
School Colors: Red (#CC0000) and Black (#1A1A1A)

Created for fundraising presentation — Phase 1 simplified design.
"""

import cadquery as cq
import math

# ============================================================
# CONSTANTS — All dimensions in inches (CAD standard)
# ============================================================
FT = 12.0  # 1 foot = 12 inches

# Building envelope
BLDG_W = 120 * FT      # 120 ft wide (X)
BLDG_D = 250 * FT      # 250 ft deep (Y)
BLDG_H = 24 * FT       # 24 ft tall  (Z)
EXT_WALL_T = 8.0       # 8-inch exterior walls
INT_WALL_T = 6.0       # 6-inch interior walls
ROOF_T = 12.0          # 12-inch roof slab
FLOOR_T = 6.0          # 6-inch floor slab

# Zone dimensions (Y measured from south/entrance end)
LOBBY_DEPTH = 25 * FT
SUPPORT_DEPTH = 40 * FT   # locker rooms, S&C, restrooms band
ARENA_DEPTH = BLDG_D - LOBBY_DEPTH - SUPPORT_DEPTH  # remainder = arena

# Support zone sub-widths (left to right across 120ft)
BOYS_LOCKER_W = 28 * FT
SC_ROOM_W = 30 * FT
GIRLS_LOCKER_W = 28 * FT
RESTROOM_CONCESSIONS_W = BLDG_W - BOYS_LOCKER_W - SC_ROOM_W - GIRLS_LOCKER_W  # 34ft

# Wrestling mats
STD_MAT_DIA = 32 * FT      # regulation practice mat ~32ft diameter (competition circle)
STD_MAT_R = STD_MAT_DIA / 2
CHAMP_MAT_DIA = 42 * FT    # championship mat ~42ft diameter
CHAMP_MAT_R = CHAMP_MAT_DIA / 2
MAT_THICKNESS = 4.0         # 4 inches thick

# Bleachers
BLEACHER_W = 12 * FT
BLEACHER_ROW_D = 2 * FT    # depth per row
BLEACHER_ROW_H = 1 * FT    # rise per row
NUM_BLEACHER_ROWS = 8

# Doors
MAIN_DOOR_W = 6 * FT
MAIN_DOOR_H = 10 * FT
STD_DOOR_W = 3 * FT
STD_DOOR_H = 7 * FT


def make_floor_slab():
    """Create the concrete floor slab at grade."""
    return (
        cq.Workplane("XY")
        .box(BLDG_W, BLDG_D, FLOOR_T)
        .translate((BLDG_W / 2, BLDG_D / 2, -FLOOR_T / 2))
    )


def make_exterior_walls():
    """Create exterior walls as a hollow rectangular shell."""
    outer = (
        cq.Workplane("XY")
        .box(BLDG_W, BLDG_D, BLDG_H)
        .translate((BLDG_W / 2, BLDG_D / 2, BLDG_H / 2))
    )
    inner = (
        cq.Workplane("XY")
        .box(BLDG_W - 2 * EXT_WALL_T, BLDG_D - 2 * EXT_WALL_T, BLDG_H + 2)
        .translate((BLDG_W / 2, BLDG_D / 2, BLDG_H / 2))
    )
    walls = outer.cut(inner)

    # Cut main entrance opening (double doors, centered on south wall)
    door_cut = (
        cq.Workplane("XY")
        .box(MAIN_DOOR_W * 2, EXT_WALL_T + 2, MAIN_DOOR_H)
        .translate((BLDG_W / 2, -1, MAIN_DOOR_H / 2))
    )
    walls = walls.cut(door_cut)

    return walls


def make_roof():
    """Create flat roof slab."""
    return (
        cq.Workplane("XY")
        .box(BLDG_W + 2 * FT, BLDG_D + 2 * FT, ROOF_T)
        .translate((BLDG_W / 2, BLDG_D / 2, BLDG_H + ROOF_T / 2))
    )


def make_interior_wall(x, y, w, d, h=None):
    """Create a single interior wall segment."""
    if h is None:
        h = BLDG_H * 0.5  # half-height interior walls for visibility
    return (
        cq.Workplane("XY")
        .box(w, d, h)
        .translate((x + w / 2, y + d / 2, h / 2))
    )


def make_interior_walls():
    """Build all interior partition walls."""
    walls = []

    # Horizontal wall separating lobby from support zone
    walls.append(make_interior_wall(
        EXT_WALL_T, LOBBY_DEPTH,
        BLDG_W - 2 * EXT_WALL_T, INT_WALL_T, BLDG_H * 0.65
    ))

    # Horizontal wall separating support zone from arena
    walls.append(make_interior_wall(
        EXT_WALL_T, LOBBY_DEPTH + SUPPORT_DEPTH,
        BLDG_W - 2 * EXT_WALL_T, INT_WALL_T, BLDG_H * 0.65
    ))

    support_y = LOBBY_DEPTH

    # Vertical wall: Boys locker | S&C
    walls.append(make_interior_wall(
        EXT_WALL_T + BOYS_LOCKER_W, support_y,
        INT_WALL_T, SUPPORT_DEPTH, BLDG_H * 0.65
    ))

    # Vertical wall: S&C | Girls locker
    walls.append(make_interior_wall(
        EXT_WALL_T + BOYS_LOCKER_W + SC_ROOM_W, support_y,
        INT_WALL_T, SUPPORT_DEPTH, BLDG_H * 0.65
    ))

    # Vertical wall: Girls locker | Restrooms/Concessions
    walls.append(make_interior_wall(
        EXT_WALL_T + BOYS_LOCKER_W + SC_ROOM_W + GIRLS_LOCKER_W, support_y,
        INT_WALL_T, SUPPORT_DEPTH, BLDG_H * 0.65
    ))

    return walls


def make_cylinder(x, y, z, radius, height):
    """Helper: create a cylinder at position."""
    return (
        cq.Workplane("XY")
        .cylinder(height, radius)
        .translate((x, y, z + height / 2))
    )


def make_wrestling_mats():
    """Create all wrestling mats on the arena floor."""
    mats = []
    arena_start_y = LOBBY_DEPTH + SUPPORT_DEPTH + INT_WALL_T
    arena_h = BLDG_D - arena_start_y - EXT_WALL_T
    arena_center_x = BLDG_W / 2
    arena_center_y = arena_start_y + arena_h / 2

    # Championship center mat (large, red)
    champ = make_cylinder(
        arena_center_x, arena_center_y, 0,
        CHAMP_MAT_R, MAT_THICKNESS
    )
    mats.append(("champ", champ))

    # Championship mat border ring (white outline effect — slightly larger, thinner)
    champ_border = make_cylinder(
        arena_center_x, arena_center_y, -0.5,
        CHAMP_MAT_R + 6, 1.0
    )
    mats.append(("champ_border", champ_border))

    # Practice mats: 2x2 grid arrangement around the championship mat
    practice_positions = []

    # Two mats flanking championship mat (left and right)
    offset_x = CHAMP_MAT_R + STD_MAT_R + 2 * FT
    practice_positions.append((arena_center_x - offset_x, arena_center_y))
    practice_positions.append((arena_center_x + offset_x, arena_center_y))

    # Two mats above championship mat
    offset_y_top = CHAMP_MAT_R + STD_MAT_R + 3 * FT
    practice_positions.append((arena_center_x - STD_MAT_R - 2 * FT, arena_center_y + offset_y_top))
    practice_positions.append((arena_center_x + STD_MAT_R + 2 * FT, arena_center_y + offset_y_top))

    for i, (px, py) in enumerate(practice_positions):
        mat = make_cylinder(px, py, 0, STD_MAT_R, MAT_THICKNESS)
        mats.append((f"practice_{i}", mat))

        # Border ring
        border = make_cylinder(px, py, -0.5, STD_MAT_R + 4, 1.0)
        mats.append((f"practice_border_{i}", border))

    return mats


def make_bleacher_block(x, y, length, facing="east"):
    """Create a stepped bleacher section.
    facing: direction the audience faces (east/west determines step direction)
    """
    assembly = cq.Assembly()

    for row in range(NUM_BLEACHER_ROWS):
        row_z = row * BLEACHER_ROW_H
        if facing == "east":
            row_x = x + row * BLEACHER_ROW_D
        else:
            row_x = x - row * BLEACHER_ROW_D

        bench = (
            cq.Workplane("XY")
            .box(BLEACHER_ROW_D - 1, length, BLEACHER_ROW_H)
            .translate((
                row_x + BLEACHER_ROW_D / 2,
                y + length / 2,
                row_z + BLEACHER_ROW_H / 2
            ))
        )
        assembly.add(bench)

    return assembly


def make_bleachers():
    """Create bleacher sections on both sides of the arena."""
    bleachers = []
    arena_start_y = LOBBY_DEPTH + SUPPORT_DEPTH + INT_WALL_T
    arena_len = BLDG_D - arena_start_y - EXT_WALL_T
    bleacher_length = arena_len - 4 * FT  # leave some margin

    # Left (west) bleachers — facing east toward center
    left_x = EXT_WALL_T + 2 * FT
    left_y = arena_start_y + 2 * FT

    for row in range(NUM_BLEACHER_ROWS):
        row_z = row * BLEACHER_ROW_H
        bench = (
            cq.Workplane("XY")
            .box(BLEACHER_ROW_D - 1, bleacher_length, BLEACHER_ROW_H)
            .translate((
                left_x + row * BLEACHER_ROW_D + BLEACHER_ROW_D / 2,
                left_y + bleacher_length / 2,
                row_z + BLEACHER_ROW_H / 2
            ))
        )
        bleachers.append(bench)

    # Right (east) bleachers — facing west toward center
    right_x = BLDG_W - EXT_WALL_T - 2 * FT
    right_y = arena_start_y + 2 * FT

    for row in range(NUM_BLEACHER_ROWS):
        row_z = row * BLEACHER_ROW_H
        bench = (
            cq.Workplane("XY")
            .box(BLEACHER_ROW_D - 1, bleacher_length, BLEACHER_ROW_H)
            .translate((
                right_x - row * BLEACHER_ROW_D - BLEACHER_ROW_D / 2,
                right_y + bleacher_length / 2,
                row_z + BLEACHER_ROW_H / 2
            ))
        )
        bleachers.append(bench)

    return bleachers


def make_entrance_canopy():
    """Create a simple entrance canopy overhang."""
    canopy = (
        cq.Workplane("XY")
        .box(30 * FT, 8 * FT, 2.0)
        .translate((BLDG_W / 2, -4 * FT, MAIN_DOOR_H + 12))
    )
    # Support columns
    cols = []
    for dx in [-12 * FT, 12 * FT]:
        col = (
            cq.Workplane("XY")
            .box(1 * FT, 1 * FT, MAIN_DOOR_H + 12)
            .translate((BLDG_W / 2 + dx, -7 * FT, (MAIN_DOOR_H + 12) / 2))
        )
        cols.append(col)

    return canopy, cols


def make_steel_beams():
    """Create exposed roof steel beams (trusses simplified as I-beams)."""
    beams = []
    beam_h = 2 * FT
    beam_w = 8.0  # 8 inches wide
    beam_z = BLDG_H - beam_h / 2 - 6  # just below roof

    # Transverse beams (spanning width) every 25 feet
    for y_offset in range(0, int(BLDG_D), int(25 * FT)):
        beam = (
            cq.Workplane("XY")
            .box(BLDG_W - 2 * EXT_WALL_T, beam_w, beam_h)
            .translate((BLDG_W / 2, y_offset + EXT_WALL_T, beam_z))
        )
        beams.append(beam)

    return beams


# ============================================================
# MAIN: Build & Export
# ============================================================
def build_model():
    """Assemble all components and export."""
    print("Building Hazel Green Trojans Sports Complex — Phase 1")
    print("=" * 60)

    # 1. Floor slab
    print("  [1/8] Floor slab...")
    floor = make_floor_slab()

    # 2. Exterior walls
    print("  [2/8] Exterior walls...")
    ext_walls = make_exterior_walls()

    # 3. Roof
    print("  [3/8] Roof slab...")
    roof = make_roof()

    # 4. Interior walls
    print("  [4/8] Interior partitions...")
    int_walls = make_interior_walls()

    # 5. Wrestling mats
    print("  [5/8] Wrestling mats...")
    mat_list = make_wrestling_mats()

    # 6. Bleachers
    print("  [6/8] Bleacher seating...")
    bleachers = make_bleachers()

    # 7. Entrance canopy
    print("  [7/8] Entrance canopy...")
    canopy, canopy_cols = make_entrance_canopy()

    # 8. Steel beams
    print("  [8/8] Steel roof beams...")
    beams = make_steel_beams()

    # --------------------------------------------------------
    # ASSEMBLY
    # --------------------------------------------------------
    print("\nAssembling model...")
    assy = cq.Assembly(name="Hazel_Green_Trojans_Complex")

    # Floor — light gray concrete
    assy.add(floor, name="floor_slab",
             color=cq.Color(0.69, 0.69, 0.69, 1.0))  # #B0B0B0

    # Exterior walls — dark charcoal/black
    assy.add(ext_walls, name="exterior_walls",
             color=cq.Color(0.10, 0.10, 0.10, 1.0))  # #1A1A1A

    # Roof — dark gray
    assy.add(roof, name="roof",
             color=cq.Color(0.25, 0.25, 0.25, 1.0))  # #404040

    # Interior walls — Trojan Red accent
    for i, wall in enumerate(int_walls):
        assy.add(wall, name=f"interior_wall_{i}",
                 color=cq.Color(0.80, 0.0, 0.0, 1.0))  # #CC0000

    # Wrestling mats
    for name, mat in mat_list:
        if "champ_border" in name:
            color = cq.Color(1.0, 1.0, 1.0, 1.0)  # white border
        elif "champ" in name:
            color = cq.Color(0.80, 0.0, 0.0, 1.0)  # red championship
        elif "border" in name:
            color = cq.Color(1.0, 1.0, 1.0, 1.0)  # white border
        else:
            color = cq.Color(0.20, 0.20, 0.20, 1.0)  # dark gray practice
        assy.add(mat, name=name, color=color)

    # Bleachers — Trojan Red seats
    for i, bench in enumerate(bleachers):
        assy.add(bench, name=f"bleacher_{i}",
                 color=cq.Color(0.80, 0.0, 0.0, 1.0))  # #CC0000

    # Entrance canopy — black
    assy.add(canopy, name="canopy",
             color=cq.Color(0.10, 0.10, 0.10, 1.0))
    for i, col in enumerate(canopy_cols):
        assy.add(col, name=f"canopy_col_{i}",
                 color=cq.Color(0.27, 0.27, 0.27, 1.0))  # #444444

    # Steel beams — dark steel gray
    for i, beam in enumerate(beams):
        assy.add(beam, name=f"steel_beam_{i}",
                 color=cq.Color(0.27, 0.27, 0.27, 1.0))  # #444444

    # --------------------------------------------------------
    # EXPORT
    # --------------------------------------------------------
    print("\nExporting files...")

    # STEP export (universal CAD)
    step_path = "/home/user/TrojanHorseAreana/Hazel_Green_Trojans_Complex.step"
    assy.save(step_path)
    print(f"  ✓ STEP: {step_path}")

    # STL export — we need to combine all solids for STL
    print("  Combining solids for STL...")
    combined = floor
    combined = combined.union(ext_walls)
    combined = combined.union(roof)
    for wall in int_walls:
        combined = combined.union(wall)
    for name, mat in mat_list:
        combined = combined.union(mat)
    for bench in bleachers:
        combined = combined.union(bench)
    combined = combined.union(canopy)
    for col in canopy_cols:
        combined = combined.union(col)
    for beam in beams:
        combined = combined.union(beam)

    stl_path = "/home/user/TrojanHorseAreana/Hazel_Green_Trojans_Complex.stl"
    cq.exporters.export(combined, stl_path, exportType="STL")
    print(f"  ✓ STL:  {stl_path}")

    print("\n✓ 3D model generation complete!")
    return assy, combined


if __name__ == "__main__":
    build_model()
