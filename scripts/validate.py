#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validate the dataset against the JSON Schema and run integrity checks.
Pure standard library (no external deps required).

Checks:
  - every record has required fields and valid enum values
  - ids are unique and kebab-case
  - comedogenic_rating in 0..5 or null
  - compatibility_rules.json groups reference real ingredient ids
Exit code is non-zero if any error is found (CI-friendly).

Usage:  python3 scripts/validate.py
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
sys.path.insert(0, HERE)
from ingredients_data import INGREDIENTS  # noqa: E402

REQUIRED = ["id", "inci_name", "common_name", "category", "description",
            "benefits", "skin_types", "comedogenic_rating", "irritancy",
            "pregnancy_safe", "vegan", "origin", "time_of_use", "evidence_level"]
ENUMS = {
    "irritancy": {"low", "medium", "high"},
    "pregnancy_safe": {"safe", "caution", "avoid"},
    "vegan": {"yes", "no", "varies"},
    "origin": {"natural", "synthetic", "both"},
    "time_of_use": {"AM", "PM", "AM/PM"},
    "evidence_level": {"strong", "moderate", "limited"},
}
SKIN_TYPES = {"all", "dry", "oily", "combination", "sensitive",
              "acne-prone", "mature", "normal"}
SLUG = re.compile(r"^[a-z0-9-]+$")


def main():
    errors = []
    seen = set()

    for i, ing in enumerate(INGREDIENTS):
        tag = ing.get("id", f"#{i}")
        for field in REQUIRED:
            if field not in ing or ing[field] in (None, "", []):
                if not (field == "comedogenic_rating" and ing.get(field) == 0):
                    errors.append(f"[{tag}] missing required field: {field}")
        if "id" in ing:
            if not SLUG.match(ing["id"]):
                errors.append(f"[{tag}] id is not kebab-case")
            if ing["id"] in seen:
                errors.append(f"[{tag}] duplicate id")
            seen.add(ing["id"])
        for field, allowed in ENUMS.items():
            if ing.get(field) not in allowed:
                errors.append(f"[{tag}] {field}={ing.get(field)!r} not in {sorted(allowed)}")
        for st in ing.get("skin_types", []):
            if st not in SKIN_TYPES:
                errors.append(f"[{tag}] invalid skin_type: {st}")
        cr = ing.get("comedogenic_rating")
        if cr is not None and not (isinstance(cr, int) and 0 <= cr <= 5):
            errors.append(f"[{tag}] comedogenic_rating out of range: {cr}")

    # cross-check compatibility rules reference real ids
    rules_path = os.path.join(DATA, "compatibility_rules.json")
    if os.path.exists(rules_path):
        with open(rules_path, encoding="utf-8") as f:
            rules = json.load(f)
        ids = {i["id"] for i in INGREDIENTS}
        for group, members in rules.get("groups", {}).items():
            for m in members:
                if m not in ids:
                    errors.append(f"[compatibility:{group}] unknown ingredient id: {m}")
        groups = set(rules.get("groups", {}))
        for r in rules.get("rules", []):
            for side in ("a", "b"):
                if r.get(side) not in groups:
                    errors.append(f"[compatibility:rule] unknown group: {r.get(side)}")

    if errors:
        print(f"VALIDATION FAILED — {len(errors)} issue(s):")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print(f"OK — {len(INGREDIENTS)} ingredients valid, ids unique, rules consistent.")


if __name__ == "__main__":
    main()
