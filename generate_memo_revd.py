"""Corrected architect transmittal memo (replaces Gemini's, which is kept as superseded). New file; nothing overwritten."""
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

st = getSampleStyleSheet()
doc = SimpleDocTemplate("Architect_Transmittal_Memo_RevD_2026-10-08.pdf", pagesize=letter,
                        leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
B = st["BodyText"]
H = st["Heading3"]
rows = [
    ("Footprint", "210 x 252 ft + NE stair tower; 2 levels", "DECIDED"),
    ("Gross area", "85,793 GSF (L1 56,861 + L2 28,933); no SF cap (D-056)", "DECIDED"),
    ("Heights", "L2 FF 17'-9\" (D-061); ring roof 32.75 ft; arena roof 42 ft; structure underside 36 ft", "L2 DECIDED / rest ASSUMED"),
    ("Seating", "2,200 = 1,100 telescopic lower + 1,100 fixed upper (21 in risers)", "DECIDED"),
    ("Event floor", "120 x 144 ft; 4 x 42 ft mats (2 x 2); chairs-only events are the design case (D-054)", "DECIDED"),
    ("Restrooms", "22 men's / 42 women's WC (chairs-only case); second core in a 30 x 56 ft east bump-out", "DECIDED (D-064/069/072)"),
    ("Storage", "2,100 SF one-storey annex, north wall (D-067)", "DECIDED; 16 ft height ASSUMED"),
    ("Code basis", "IBC 2021 (county on 2018, State Fire Marshal on 2021)", "ASSUMED - AHJ to confirm (D-008)"),
    ("Occupancy / occupant load", "Building official assigns (IBC 1004.5); see R-007", "OPEN"),
    ("Structure / MEP", "No structural system, grid, truss, solar, storage, cistern or generator is decided", "OPEN"),
]
cells = [("Item", "Value", "Status")] + [(Paragraph(a, B), Paragraph(b, B), Paragraph(c, B)) for a, b, c in rows]
t = Table(cells, colWidths=[100, 280, 130])
t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                       ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#CC0000")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white)]))
body = [
    Paragraph("<b>PRELIMINARY - CONCEPTUAL DESIGN - NOT FOR CONSTRUCTION</b>", st["Title"]),
    Paragraph("<b>TO:</b> Alabama-registered Architect of Record<br/><b>FROM:</b> Shane Brazelton, Owner<br/>"
              "<b>DATE:</b> October 8, 2026<br/><b>RE:</b> Trojan Horse Arena - Hazel Green Regional Athletic Complex - "
              "Phase 2 Schematic Set Rev D (program package)", B),
    Spacer(1, 8),
    Paragraph("1. Purpose", H),
    Paragraph("This is a schematic program package, not a permit set. Alabama requires a registered architect for this building, and I am "
              "asking your firm to take it from here. Nothing in it is stamped, engineered or code-reviewed. The site is not chosen (D-006), "
              "so no jurisdiction-specific review has been done.", B),
    Paragraph("2. Enclosed: approved, frozen set (13 sheets)", H),
    Paragraph("Phase2_Schematic_Set_RevD.pdf: P2-G-001 C, G-002 D, G-003 K, A-101 J, A-102 F, A-103 D, A-111 D, A-201 I, A-301 D, A-302 C, "
              "A-401 D, A-901 D, C-101 F. Every sheet is labelled PRELIMINARY - NOT FOR CONSTRUCTION. Decisions are logged and every value is "
              "labelled DECIDED, ASSUMED or CITED.", B),
    Paragraph("3. Locked facts and status", H),
    t,
    Paragraph("4. Owner design intent (concept, not in the set)", H),
    Paragraph("I intend the arena to echo the SRM Concrete corporate headquarters design language (radiused forms, board-formed concrete, "
              "glass) with metal-building pop-outs (D-074). These are concept images only; the approved plan is rectangular. Please advise "
              "what a curved envelope does to the tiers, egress and structure.", B),
    Paragraph("5. Open items I need your help with", H),
    Paragraph("Parcel and AHJ pre-application (D-006, D-008); code edition; occupancy and occupant load; upper-tier structure depth (7'-6\" "
              "clear under the front row needs a tier structure of 1'-6\" or less); total mechanical about 4.1% against a 5% planning figure; "
              "X7 / X11 discharge paths; and a GC or estimator to price the set (working number $39M mid, $28-57M, excluding land; planning "
              "only, not for lender or donor use).", B),
]
doc.build(body)
print("wrote Architect_Transmittal_Memo_RevD_2026-10-08.pdf")
