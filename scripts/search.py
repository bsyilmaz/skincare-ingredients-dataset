#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command-line explorer for the Skincare Ingredients Dataset.

Examples:
  python3 scripts/search.py niacinamide              # find an ingredient
  python3 scripts/search.py --category Antioxidant   # list a category
  python3 scripts/search.py --skin acne-prone        # filter by skin type
  python3 scripts/search.py --pregnancy safe         # filter by pregnancy safety
  python3 scripts/search.py --check retinol "salicylic acid"   # mixing check
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
sys.path.insert(0, HERE)
from ingredients_data import INGREDIENTS  # noqa: E402


def find(query):
    q = query.lower()
    hits = []
    for ing in INGREDIENTS:
        hay = " ".join([ing["id"], ing["inci_name"], ing["common_name"],
                        " ".join(ing.get("also_known_as", []))]).lower()
        if q in hay:
            hits.append(ing)
    return hits


def show(ing):
    print(f"\n== {ing['common_name']}  ({ing['inci_name']}) ==")
    print(f"   {ing['description']}")
    print(f"   Categories : {', '.join(ing['category'])}")
    print(f"   Benefits   : {', '.join(ing['benefits'])}")
    print(f"   Skin types : {', '.join(ing['skin_types'])}")
    print(f"   Comedogenic: {ing['comedogenic_rating']}/5   Irritancy: {ing['irritancy']}")
    print(f"   Pregnancy  : {ing['pregnancy_safe']}   Use: {ing['time_of_use']}   Evidence: {ing['evidence_level']}")
    if ing.get("pairs_well_with"):
        print(f"   Pairs with : {', '.join(ing['pairs_well_with'])}")
    if ing.get("avoid_with"):
        print(f"   Avoid with : {', '.join(ing['avoid_with'])}")


def groups_for(ing_id, rules):
    return [g for g, members in rules["groups"].items() if ing_id in members]


def check(name_a, name_b):
    a = find(name_a)
    b = find(name_b)
    if not a or not b:
        print("Could not resolve one of the ingredients.")
        return
    a, b = a[0], b[0]
    with open(os.path.join(DATA, "compatibility_rules.json"), encoding="utf-8") as f:
        rules = json.load(f)
    ga, gb = groups_for(a["id"], rules), groups_for(b["id"], rules)
    found = []
    for r in rules["rules"]:
        if (r["a"] in ga and r["b"] in gb) or (r["a"] in gb and r["b"] in ga):
            found.append(r)
    print(f"\nMixing {a['common_name']} + {b['common_name']}:")
    if not found:
        print("  No specific rule found — generally fine, but patch test new combos.")
    for r in found:
        print(f"  [{r['severity'].upper()}] {r['reason']}")
        print(f"          -> {r['recommendation']}")


def main():
    p = argparse.ArgumentParser(description="Explore the skincare ingredients dataset.")
    p.add_argument("query", nargs="?", help="free-text search")
    p.add_argument("--category")
    p.add_argument("--skin")
    p.add_argument("--pregnancy")
    p.add_argument("--check", nargs=2, metavar=("A", "B"))
    args = p.parse_args()

    if args.check:
        check(*args.check)
        return
    results = INGREDIENTS
    if args.category:
        results = [i for i in results if args.category.lower() in
                   [c.lower() for c in i["category"]]]
    if args.skin:
        results = [i for i in results if args.skin.lower() in
                   [s.lower() for s in i["skin_types"]]]
    if args.pregnancy:
        results = [i for i in results if i["pregnancy_safe"] == args.pregnancy.lower()]
    if args.query:
        results = [i for i in results if i in find(args.query)]

    if not results:
        print("No matches.")
        return
    if len(results) > 8 and not args.query:
        print(f"{len(results)} matches:")
        for i in results:
            print(f"  - {i['common_name']} ({i['inci_name']}) — {', '.join(i['category'][:2])}")
    else:
        for i in results:
            show(i)


if __name__ == "__main__":
    main()
