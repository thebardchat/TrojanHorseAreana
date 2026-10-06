The KEYSTONE drawing-sheet frame: a 1.6 pt border, a full-width PRELIMINARY stamp band, and an eight-cell title block along the bottom.

**When to use:** every PDF/DXF sheet. It is layout only; all values come from the `params/phase*.yaml` file for the sheet.

**Rules**
- Border `lw-sheet-border`, stamp band `lw-stamp-band`, cell dividers `lw-cell`, all in `ink` on `surface`. No fills, no color. `brand` is reserved for the drawing itself.
- Stamp text is exactly `PRELIMINARY — CONCEPTUAL DESIGN — NOT FOR CONSTRUCTION`, `sheet-stamp`, centered, on every sheet.
- Cells, left to right with width shares 4.7 / 1.5 / 3.1 / 0.9 / 1.45 / 0.75 / 2.1 / 1.5: PROJECT, PHASE, SHEET TITLE, SCALE, DATE, REV, DRAWN BY, SHEET. Labels `sheet-note`; values `sheet-cell`; the sheet number `sheet-number`, centered.
- Layers: `G-ANNO-TTLB` for the frame, `A-ANNO-TEXT` for text; DXF color 7 (prints black).
- Margin 0.5 in, title block 1.35 in tall, stamp band 0.5 in.

**The consumer supplies** project, phase, title, scale, date, revision, drafter and sheet number.
