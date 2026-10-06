# Trojan Horse Arena

> Building Champions, One Mat at a Time.

The visual language of the Hazel Green Trojans Sports Complex project (North Alabama Regional Athletic Complex): school red and black on architectural drawing sheets, and a neon-on-dark look for the web pages and 3D viewer. Extracted from `thebardchat/TrojanHorseAreana` (render scripts, `index.html`, the 3D viewer, and the KEYSTONE sheet kit in `blueprints/`).

This project operates under the [ShaneTheBrain Constitution](https://github.com/thebardchat/constitution/blob/main/CONSTITUTION.md).

## One brand, two themes

| Theme | Where it is used | Ground |
|---|---|---|
| `paper` | PDF and PNG drawing sheets, floor plans, elevations, print | `surface` #f5f5f0 with white `panel` |
| `arena` | `index.html` landing page, the 3D viewer | `surface` #080c10 with `panel` #0d1520 |

Both share the same role names (`surface`, `panel`, `ink`, `ink-muted`, `brand`, `accent`). Only the values change, so a component written against the tokens works in either.

## Content fundamentals

- **Voice:** short, declarative, sports-program confident. Taglines are three beats: "Strategy. Deception. Victory." and "Building Champions, One Mat at a Time."
- **Casing:** headings, buttons, nav links and labels are UPPERCASE with tracking. Body copy is sentence case.
- **Labels:** web section labels are written as code comments, `// Core Features`. Do not decorate them further.
- **Sheets:** every sheet carries the stamp `PRELIMINARY — CONCEPTUAL DESIGN — NOT FOR CONSTRUCTION` and never says anything stronger than that. Dimensions are written `120 ft`, `32ft Dia.`, `1" = 250'`.
- **Credit line:** `Built together, not alone.` and `Hazel Green, AL` in the footer.

## Visual foundations

- **Color:** red is the only loud color. Use `brand` for the one thing that matters on a screen or sheet; use `ink` and `ink-muted` for everything else. `accent` (yellow on arena, gold fill on paper) marks labels and badges. `success` and `violet` are decoration for feature accents on arena, one per card.
- **Contrast:** `ink` and `ink-muted` hold 4.5:1 on `surface` and `panel` in both themes. `brand` text holds it on `surface` in both themes. `accent` on paper and `violet` on paper are fills only. `brand-deep` is a fill or border, never text.
- **Shape:** square. `radius-sharp` (0) everywhere on the web. The only rounding is `radius-glass` on the 3D viewer's info panel. The only circles are wrestling mats on plans: 42 ft championship, 32 ft practice.
- **Lines:** drawings are built from line weights, not shadows. Use `lw-exterior` for the building outline, `lw-sheet-border` for the sheet frame, `lw-detail` for ordinary edges, `lw-hairline` for tags.
- **Glow:** arena only. `glow-brand` under a primary button, `glow-accent` on the pulsing badge. Never on paper.
- **Backdrop:** arena pages carry a 40px grid of 3%-opacity cyan lines behind content. Sections are separated by a 1px gradient rule, `brand` fading to transparent at 25% opacity.
- **Motion:** one pulse on the accent badge (2s, box-shadow only), color transitions at 0.2s, and a 2–3px lift on hover. Nothing else moves.
- **Layout:** sections max 1000px wide with `space-16` vertical padding and `space-8` gutters. Feature grids use `minmax(240px, 1fr)` with `space-5` gaps.
- **Type:** arena is monospace (`arena` family, Courier New), sheets are DejaVu Sans, the 3D viewer is Inter. Do not mix them on one surface.

## Iconography and marks

- The `THA` mark ships in three single-ink versions in `blueprints/brand/` (see `assets/Logos/README.md`): red (#cc0000), black (#1a1a1a), white. Use red on paper, white on dark or on a `brand` fill, black for one-color print. Never recolor, outline or stretch it. Keep clear space of at least one quarter of the mark's width.
- The web pages use the stadium emoji as a stand-in logo in `index.html`. That is a placeholder; prefer the THA mark.
- No icon set exists in the repo. Use text labels.

## Components

Four static component cards document the patterns that exist in the source: `Button`, `Badge`, `StatBlock`, `TitleBlock`. They are hand-written from `index.html` and `blueprints/shared/titleblock.py`; there is no compiled library to bundle.

## Using it

- CSS: every token is a custom property (`var(--brand)`, `var(--space-6)`, `var(--font-arena)`). Switch theme with `data-theme="paper"` or `data-theme="arena"` on `<html>`.
- Python drawings: the same hexes are constants in `render_floorplan.py`, `render_3d_views.py`, and `blueprints/shared/titleblock.py`. Match `school-red`, `school-black`, `plan-*`.

## Not extracted

- `index.html` uses `color-mix()` in glows and `rgba()` cyan for the grid. Both are rebuilt here as literal shadow and described above, not tokenized.
- The 3D viewer's blue (`rgba(0,170,255)`) drop-zone overlay is a tool state, not part of the brand, and is left out.
- Phase 2 tints (`plan-tint-*`, `brick*`) were read from script palettes; their exact room mapping is inferred.
- The blueprint scripts include many one-off hexes (greys, rooms). Only the ones repeated across scripts became tokens.
- No font files live in the repo; all three families are system or hosted fonts.
