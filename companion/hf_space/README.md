---
title: Farmer Intermediary Margin Lab
emoji: 🧪
colorFrom: blue
colorTo: green
sdk: static
app_file: index.html
short_description: Explore a synthetic margin-rule model and planned 2x2 study.
---

# Farmer–Intermediary Margin Lab

An interactive, assumption-based companion to the PS1 proposal. It compares a fixed margin rule with an intermediary-chosen rule and shows how modeled farmer participation and completed units change with coordination cost.

Live Space: [Farmer–Intermediary Margin Lab](https://huggingface.co/spaces/dku-comsci-econ206-2026/Farmer_Intermediary_Margin_Lab)

**This is a synthetic teaching simulation, not a deployed behavioral experiment or evidence about real households.** No responses are collected or sent to a server. The reputation parameter is set to zero by default and should be changed only after a behavioral estimate is available; any nonzero value is a scenario assumption.

## Research design represented here

The proposed 2 × 2 study varies (1) fixed versus intermediary-chosen margin rule and (2) sparse versus verified seller-history information. In the planned vignette, the listed household price, product identity, quality evidence, quantity, and delivery are held constant across cells. Outcomes include purchase choice, trust, perceived price fairness, expected quality, and willingness to pay. The design can distinguish reputation information from changes in perceived price or product quality.

## Files

- `index.html` — static interface
- `model.js` — model calculations; no external packages

The app runs as a static Hugging Face Space and can also be opened locally by opening `index.html` in a browser.
