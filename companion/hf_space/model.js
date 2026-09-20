(() => {
  "use strict";
  const BASE = { w: 6, c: 4, effortCost: 30, demandScale: 12, chokeMargin: 4 };
  const money = (x) => Number(x).toFixed(1);

  function quantity(m, e, rho, verified) {
    return BASE.demandScale * e * Math.max(0, BASE.chokeMargin - m) * (verified ? 1 + rho : 1);
  }
  function profit(m, e, rho, verified) {
    return m * quantity(m, e, rho, verified) - BASE.effortCost * e * e;
  }
  function optimize(rule, rho, verified) {
    let best = { profit: -Infinity, m: 0, e: 0 };
    if (rule === "Fixed") {
      for (let i = 0; i <= 100; i += 1) {
        const e = i / 100, m = 1, value = profit(m, e, rho, verified);
        if (value > best.profit) best = { profit: value, m, e };
      }
    } else {
      for (let j = 0; j <= 80; j += 1) {
        const m = j * 0.05;
        for (let i = 0; i <= 100; i += 1) {
          const e = i / 100, value = profit(m, e, rho, verified);
          if (value > best.profit) best = { profit: value, m, e };
        }
      }
    }
    return best;
  }
  function evaluate(rule, information, K, rho) {
    const verified = information === "Verified";
    const choice = optimize(rule, rho, verified);
    const unitsIfJoin = quantity(choice.m, choice.e, rho, verified);
    const farmerIfJoin = (BASE.w - BASE.c) * unitsIfJoin - K;
    const joins = farmerIfJoin >= 0;
    return {
      rule, information, m: choice.m, e: choice.e,
      completed_units: joins ? unitsIfJoin : 0,
      farmer_net: joins ? farmerIfJoin : 0,
      farmer_if_join: farmerIfJoin,
      intermediary_profit: joins ? choice.profit : 0,
      joins
    };
  }
  function render() {
    const K = Number(document.getElementById("cost").value);
    const rho = Number(document.getElementById("rho").value);
    const information = document.getElementById("information").value;
    const priority = document.getElementById("priority").value;
    document.getElementById("cost-value").textContent = money(K);
    document.getElementById("rho-value").textContent = `${(rho * 100).toFixed(0)}%`;

    const rows = ["Sparse", "Verified"].flatMap((info) => ["Fixed", "Chosen"].map((rule) => evaluate(rule, info, K, rho)));
    document.getElementById("results").innerHTML = rows.map((r) => `<tr>
      <td>${r.information}</td><td>${r.rule}</td><td class="num">${money(r.m)}</td><td class="num">${money(r.e)}</td>
      <td class="num">${money(r.completed_units)}</td><td class="num">${money(r.farmer_net)}</td><td class="num">${money(r.intermediary_profit)}</td>
      <td class="status">${r.joins ? "Participates" : "No trade"}</td></tr>`).join("");

    const pair = rows.filter((r) => r.information === information);
    const [fixed, chosen] = pair;
    const labels = { completed_units: "modeled completed units", farmer_net: "modeled farmer net earnings", intermediary_profit: "modeled intermediary profit" };
    const a = fixed[priority], b = chosen[priority];
    let comparison;
    if (Math.abs(a - b) < 1e-8) comparison = `The two rules tie on ${labels[priority]} in this scenario.`;
    else comparison = `${a > b ? "Fixed rule" : "Intermediary-chosen rule"} ranks higher on ${labels[priority]} in this scenario.`;
    const rhoNote = information === "Verified" && rho > 0 ? ` The verified-history demand lift is set to ${(rho * 100).toFixed(0)}% as a hypothetical assumption.` : " The verified-history demand lift is zero in this baseline.";
    document.getElementById("recommendation").innerHTML = `<strong>Scenario result:</strong> ${comparison} At K = ${money(K)}, using ${information.toLowerCase()} seller history.${rhoNote} This is a model ranking, not an empirical recommendation.`;

    const cutoffs = ["Fixed", "Chosen"].map((rule) => {
      const opt = optimize(rule, rho, information === "Verified");
      return `${rule}: K ≤ ${money((BASE.w - BASE.c) * quantity(opt.m, opt.e, rho, information === "Verified"))}`;
    });
    document.getElementById("thresholds").textContent = `For the selected information condition (${information}), the model's current participation limits are ${cutoffs.join("; ")}.`;
  }
  ["cost", "rho", "information", "priority"].forEach((id) => document.getElementById(id).addEventListener("input", render));
  ["information", "priority"].forEach((id) => document.getElementById(id).addEventListener("change", render));
  render();
})();
