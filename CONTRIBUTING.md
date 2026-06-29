# Contributing

Thanks for helping build the most useful open skincare ingredient dataset. **Adding a single ingredient is a great first contribution.** 🧴

## How to add or edit an ingredient

1. Open [`scripts/ingredients_data.py`](./scripts/ingredients_data.py).
2. Copy an existing record and edit the fields. Keep them accurate and **cite your source in the PR description** (a textbook, a peer-reviewed study, INCIDecoder, the CosIng database, manufacturer technical docs, etc.).
3. Run the build and validation:
   ```bash
   python3 scripts/build.py
   python3 scripts/validate.py
   ```
4. Open a pull request. Done!

> You only edit `ingredients_data.py`. Everything in `data/` (JSON, CSV, by-category, stats) is **generated** by `build.py` — don't edit those by hand.

## Field rules

| Field | Rule |
|---|---|
| `id` | unique, kebab-case (`alpha-arbutin`) |
| `inci_name` | the official INCI label name |
| `category` | use existing categories from [`data/categories.json`](./data/categories.json) where possible |
| `skin_types` | only: `all, dry, oily, combination, sensitive, acne-prone, mature, normal` |
| `comedogenic_rating` | integer `0`–`5`, or `null` if not applicable |
| `irritancy` | `low` / `medium` / `high` |
| `pregnancy_safe` | `safe` / `caution` / `avoid` |
| `vegan` | `yes` / `no` / `varies` |
| `origin` | `natural` / `synthetic` / `both` |
| `time_of_use` | `AM` / `PM` / `AM/PM` |
| `evidence_level` | `strong` / `moderate` / `limited` — be honest; lots of botanicals are `limited` |

`validate.py` enforces all of the above and will fail CI if something is off.

## Adding a compatibility rule

Edit [`data/compatibility_rules.json`](./data/compatibility_rules.json). Add the ingredient `id` to a `group` (or create a new group), then add a rule between two groups with a `severity`, `reason` and `recommendation`. Run `validate.py` to confirm every referenced id exists.

## Quality bar

- **Accuracy over volume.** A wrong comedogenic rating or a bad pregnancy flag is worse than a missing ingredient.
- **Plain language.** Descriptions should read like good product copy, not a chemistry paper.
- **No medical claims.** We describe cosmetic benefits, not cures.
- **Neutral on brands.** This dataset is about ingredients, not products.

## Ideas that would really help

- Multilingual `common_name` fields (start with one language you speak)
- `cas_number` / `cosing_id` cross-references
- More compatibility rules with citations
- Demo UI translations

By contributing you agree your work is released under the repo's [MIT License](./LICENSE).
