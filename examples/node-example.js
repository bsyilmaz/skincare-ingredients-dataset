/**
 * Node.js example — load the dataset and do useful things with it.
 * Run:  node examples/node-example.js
 */
const fs = require("fs");
const path = require("path");

const data = JSON.parse(
  fs.readFileSync(path.join(__dirname, "../data/ingredients.json"), "utf-8")
);
const rules = JSON.parse(
  fs.readFileSync(path.join(__dirname, "../data/compatibility_rules.json"), "utf-8")
);

// 1. Build a routine for acne-prone, pregnancy-safe skin
const acneSafe = data.filter(
  (i) => i.skin_types.includes("acne-prone") && i.pregnancy_safe === "safe"
);
console.log(`\n${acneSafe.length} acne-friendly, pregnancy-safe ingredients:`);
console.log(acneSafe.map((i) => i.common_name).join(", "));

// 2. Find everything to avoid mixing with retinol
const groupsFor = (id) =>
  Object.entries(rules.groups)
    .filter(([, members]) => members.includes(id))
    .map(([g]) => g);

function check(idA, idB) {
  const ga = groupsFor(idA);
  const gb = groupsFor(idB);
  return rules.rules.filter(
    (r) =>
      (ga.includes(r.a) && gb.includes(r.b)) ||
      (gb.includes(r.a) && ga.includes(r.b))
  );
}

console.log("\nRetinol + Glycolic Acid:");
check("retinol", "glycolic-acid").forEach((r) =>
  console.log(`  [${r.severity}] ${r.recommendation}`)
);

// 3. Top non-comedogenic hydrators
const hydrators = data
  .filter((i) => i.category.includes("Humectant") && i.comedogenic_rating === 0)
  .map((i) => i.common_name);
console.log(`\nNon-comedogenic humectants: ${hydrators.join(", ")}`);
