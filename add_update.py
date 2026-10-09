#!/usr/bin/env python3
"""Add an entry to updates.json (the site reads it live; commit + push to main to publish).

Examples
  python add_update.py "Roof framing study" "First pass at the long-span roof." --tag Concept --image concepts/roof.png
  python add_update.py --gallery concepts/roof.png "Roof framing" "Truss layout over the bowl."
  python add_update.py --upcoming "Wind study" "Engineer to review" --status Open
"""
import argparse
import datetime
import json

p = argparse.ArgumentParser()
p.add_argument("title")
p.add_argument("text")
p.add_argument("--tag", default="Update")
p.add_argument("--image")
p.add_argument("--gallery", metavar="SRC", help="add to the gallery instead: SRC, then title and caption as the two positionals")
p.add_argument("--upcoming", action="store_true", help="add to the upcoming list instead")
p.add_argument("--status", default="Open")
a = p.parse_args()

with open("updates.json", encoding="utf-8") as f:
    d = json.load(f)
today = datetime.date.today().isoformat()
if a.gallery:
    d["gallery"].insert(0, {"src": a.gallery, "title": a.title, "caption": a.text})
elif a.upcoming:
    d["upcoming"].append({"title": a.title, "text": a.text, "status": a.status})
else:
    e = {"date": today, "tag": a.tag, "title": a.title, "text": a.text}
    if a.image:
        e["image"] = a.image
    d["updates"].insert(0, e)
d["updated"] = today
with open("updates.json", "w", encoding="utf-8") as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
    f.write("\n")
print("updates.json updated", today)
