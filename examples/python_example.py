"""
Python example — load the dataset and answer real product questions.
Run:  python3 examples/python_example.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = json.load(open(os.path.join(ROOT, "data", "ingredients.json"), encoding="utf-8"))
rules = json.load(open(os.path.join(ROOT, "data", "compatibility_rules.json"), encoding="utf-8"))

# 1. "I'm pregnant — what should I avoid?"
avoid = [i["common_name"] for i in data if i["pregnancy_safe"] == "avoid"]
print("Avoid during pregnancy:", ", ".join(avoid))

# 2. Brightening ingredients backed by strong evidence
bright = [i["common_name"] for i in data
          if "Skin-brightening" in i["category"] and i["evidence_level"] != "limited"]
print("\nEvidence-backed brighteners:", ", ".join(bright))

# 3. A tiny recommender: score ingredients for an oily, acne-prone user
def score(ing, skin="acne-prone"):
    s = 0
    if skin in ing["skin_types"]:
        s += 2
    if ing["comedogenic_rating"] == 0:
        s += 1
    if "Anti-acne" in ing["category"]:
        s += 2
    if ing["irritancy"] == "high":
        s -= 1
    return s

ranked = sorted(data, key=lambda i: score(i), reverse=True)[:8]
print("\nTop picks for oily / acne-prone skin:")
for i in ranked:
    print(f"  - {i['common_name']} (score {score(i)})")

# 4. Compatibility check helper
def groups_for(ing_id):
    return [g for g, m in rules["groups"].items() if ing_id in m]

def check(a, b):
    ga, gb = groups_for(a), groups_for(b)
    return [r for r in rules["rules"]
            if (r["a"] in ga and r["b"] in gb) or (r["a"] in gb and r["b"] in ga)]

print("\nVitamin C + Niacinamide:")
for r in check("ascorbic-acid", "niacinamide"):
    print(f"  [{r['severity']}] {r['reason']}")
