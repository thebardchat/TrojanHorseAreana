#!/usr/bin/env python3
"""
FreeCAD Import Macro — Run this inside FreeCAD to convert STEP -> FCStd

Usage:
  1. Open FreeCAD
  2. Go to Macro > Macros... > Run Macro
  3. Select this file
  4. The STEP file will be imported and saved as .FCStd

Alternatively, from FreeCAD's Python console:
  exec(open("import_to_freecad.py").read())
"""

import os

try:
    import FreeCAD
    import Part
    import ImportGui

    script_dir = os.path.dirname(os.path.abspath(__file__))
    step_file = os.path.join(script_dir, "Hazel_Green_Trojans_Complex.step")
    fcstd_file = os.path.join(script_dir, "Hazel_Green_Trojans_Complex.FCStd")

    # Create new document
    doc = FreeCAD.newDocument("Hazel_Green_Trojans_Complex")

    # Import STEP file
    ImportGui.insert(step_file, doc.Name)

    # Save as FCStd
    doc.saveAs(fcstd_file)
    FreeCAD.Console.PrintMessage(f"\n✓ Saved: {fcstd_file}\n")
    FreeCAD.Console.PrintMessage("Hazel Green Trojans Sports Complex loaded successfully!\n")

except ImportError:
    print("ERROR: This script must be run inside FreeCAD.")
    print("  1. Open FreeCAD")
    print("  2. Macro > Execute Macro > select this file")
    print("  3. Or run from FreeCAD command line:")
    print("     freecadcmd import_to_freecad.py")
