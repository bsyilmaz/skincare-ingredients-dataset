#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script: turns scripts/ingredients_data.py into all distributable formats.

Outputs (in data/):
  ingredients.json        pretty-printed full dataset
  ingredients.min.json    minified full dataset
  ingredients.csv         flattened spreadsheet-friendly version
  by-category/<slug>.json one file per functional category
  stats.json              dataset statistics (also used by the README/demo)

Usage:  python3 scripts/build.py
"""
import csv
import json
import os
import re
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
BY_CAT = os.path.join(DATA, "by-category")

import sys
sys.path.insert(0, HERE)
from ingredients_data import INGREDIENTS  # noqa: E402

LIST_FIELDS = ["also_known_as", "category", "benefits", "skin_types",
               "concerns", "pairs_well_with", "avoid_with"]


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def main():
    os.makedirs(BY_CAT, exist_ok=True)
    data = sorted(INGREDIENTS, key=lambda x: x["common_name"].lower())

    # 1. Full JSON (pretty + minified)
    with open(os.path.join(DATA, "ingredients.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    with open(os.path.join(DATA, "ingredients.min.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

    # 2. CSV (flatten list fields with "; ")
    fields = list(data[0].keys())
    with open(os.path.join(DATA, "ingredients.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in data:
            flat = dict(row)
            for k in LIST_FIELDS:
                if isinstance(flat.get(k), list):
                    flat[k] = "; ".join(flat[k])
            w.writerow(flat)

    # 3. Per-category files
    cat_map = defaultdict(list)
    for ing in data:
        for c in ing["category"]:
            cat_map[c].append(ing)
    # clear old category files (best-effort; ignore if FS blocks deletion)
    current = {f"{slug(c)}.json" for c in cat_map}
    for old in os.listdir(BY_CAT):
        if old.endswith(".json") and old not in current:
            try:
                os.remove(os.path.join(BY_CAT, old))
            except OSError:
                pass
    for cat, items in cat_map.items():
        with open(os.path.join(BY_CAT, f"{slug(cat)}.json"), "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)

    # 4. Stats
    stats = {
        "total_ingredients": len(data),
        "total_categories": len(cat_map),
        "by_category": dict(Counter(
            c for ing in data for c in ing["category"]).most_common()),
        "by_pregnancy_safety": dict(Counter(i["pregnancy_safe"] for i in data)),
        "by_origin": dict(Counter(i["origin"] for i in data)),
        "by_evidence_level": dict(Counter(i["evidence_level"] for i in data)),
        "vegan_friendly": sum(1 for i in data if i["vegan"] == "yes"),
        "non_comedogenic": sum(1 for i in data if i.get("comedogenic_rating") == 0),
    }
    with open(os.path.join(DATA, "stats.json"), "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    # 5. Self-contained demo (inject data into the template)
    demo_dir = os.path.join(ROOT, "demo")
    tpl_path = os.path.join(demo_dir, "_template.html")
    if os.path.exists(tpl_path):
        with open(tpl_path, encoding="utf-8") as f:
            tpl = f.read()
        rules_path = os.path.join(DATA, "compatibility_rules.json")
        rules_json = open(rules_path, encoding="utf-8").read() if os.path.exists(rules_path) else "{}"
        ing_json = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        html = tpl.replace("__INGREDIENTS_JSON__", ing_json).replace("__RULES_JSON__", rules_json)
        with open(os.path.join(demo_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)

    print(f"Built {stats['total_ingredients']} ingredients across "
          f"{stats['total_categories']} categories.")
    print(f"  data/ingredients.json / .min.json / .csv")
    print(f"  data/by-category/  ({len(cat_map)} files)")
    print(f"  data/stats.json")
    print(f"  demo/index.html")


if __name__ == "__main__":
    main()
