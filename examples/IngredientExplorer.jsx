/**
 * IngredientExplorer — a drop-in React component for the Skincare Ingredients Dataset.
 *
 * Usage:
 *   import ingredients from "../data/ingredients.json";
 *   <IngredientExplorer ingredients={ingredients} />
 *
 * No required props besides `ingredients`. Tailwind classes used for styling;
 * swap for your own if you don't use Tailwind.
 */
import { useMemo, useState } from "react";

export default function IngredientExplorer({ ingredients = [] }) {
  const [query, setQuery] = useState("");
  const [skin, setSkin] = useState("all-skin");

  const skinTypes = useMemo(() => {
    const s = new Set();
    ingredients.forEach((i) => i.skin_types.forEach((t) => s.add(t)));
    return ["all-skin", ...[...s].sort()];
  }, [ingredients]);

  const results = useMemo(() => {
    const q = query.trim().toLowerCase();
    return ingredients.filter((i) => {
      const matchesQuery =
        !q ||
        i.common_name.toLowerCase().includes(q) ||
        i.inci_name.toLowerCase().includes(q) ||
        (i.also_known_as || []).some((a) => a.toLowerCase().includes(q));
      const matchesSkin = skin === "all-skin" || i.skin_types.includes(skin);
      return matchesQuery && matchesSkin;
    });
  }, [ingredients, query, skin]);

  const pregnancyBadge = { safe: "✅", caution: "⚠️", avoid: "⛔" };

  return (
    <div className="max-w-3xl mx-auto p-4">
      <div className="flex flex-col sm:flex-row gap-3 mb-5">
        <input
          className="flex-1 border rounded-lg px-3 py-2"
          placeholder="Search e.g. niacinamide, retinol, vitamin C…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <select
          className="border rounded-lg px-3 py-2"
          value={skin}
          onChange={(e) => setSkin(e.target.value)}
        >
          {skinTypes.map((t) => (
            <option key={t} value={t}>
              {t === "all-skin" ? "All skin types" : t}
            </option>
          ))}
        </select>
      </div>

      <p className="text-sm text-gray-500 mb-3">{results.length} ingredients</p>

      <div className="grid gap-3">
        {results.map((i) => (
          <div key={i.id} className="border rounded-xl p-4 shadow-sm">
            <div className="flex items-center justify-between">
              <h3 className="font-semibold text-lg">{i.common_name}</h3>
              <span className="text-sm">
                {pregnancyBadge[i.pregnancy_safe]} {i.time_of_use}
              </span>
            </div>
            <p className="text-xs text-gray-500 mb-2">{i.inci_name}</p>
            <p className="text-sm mb-3">{i.description}</p>
            <div className="flex flex-wrap gap-2 text-xs">
              {i.category.map((c) => (
                <span key={c} className="bg-pink-100 text-pink-800 rounded-full px-2 py-0.5">
                  {c}
                </span>
              ))}
              <span className="bg-gray-100 rounded-full px-2 py-0.5">
                Comedogenic {i.comedogenic_rating}/5
              </span>
              <span className="bg-gray-100 rounded-full px-2 py-0.5">
                Irritancy: {i.irritancy}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
