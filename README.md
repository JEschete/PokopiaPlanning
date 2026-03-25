# Pokemon Pokopia — City Planning Resources

Planning toolkit for building optimized, aesthetic cities across all Pokopia areas.

---

## Planning

Active city-building documents — where the design work lives.

| File | Description |
|------|-------------|
| [Wasteland House Groups](planning/Wasteland%20House%20Groups.md) | Houses 1–19 — Withered Wastelands |
| [Beach House Groups](planning/Beach%20House%20Groups.md) | Houses 20–37 — Bleak Beach |
| [Ridges House Groups](planning/Ridges%20House%20Groups.md) | Houses 38–58 — Rocky Ridges |
| [Skylands House Groups](planning/Skylands%20House%20Groups.md) | Houses 59–78, 87 — Sparkling Skylands |
| [Pallet House Groups](planning/Pallet%20House%20Groups.md) | Houses 79–86 — Palette Town |
| [Landscape & Building Plan](planning/Landscape%20%26%20Building%20Plan.md) | Master layout guide: district maps, architecture styles, water/lava features, urban zones, and lighting per area |
| [City Planning](planning/City%20Planning.txt) | Working input file — paste Pokemon batches here for house group analysis |

### Area Summary

| Area | Size | Houses | Habitat Types |
|------|------|--------|---------------|
| Withered Wastelands | 240x240 | 1–19 (19) | Bright, Dark, Dry, Humid, Warm |
| Bleak Beach | 272x272 | 20–37 (18) | Bright, Cool*, Dark, Humid, Warm |
| Rocky Ridges | 272x272 | 38–58 (21) | Bright, Cool, Dark, Dry, Humid, Warm |
| Sparkling Skylands | 352x352 | 59–78, 87 (21) | Bright, Cool, Dark, Dry, Humid, Warm |
| Palette Town | 384x384 | 79–86 (8) | Bright, Cool*, Dark, Humid, Warm |

*\* Cool solos flagged for potential cross-area consolidation (Meowth, Glaceon)*

---

## Reference

Game data and lookup tables scraped/compiled from the wiki.

| File | Description |
|------|-------------|
| [Pokopia.csv](reference/Pokopia.csv) | Full database of 305 Pokemon — number, name, location, habitat, favorites, specialties |
| [Item List](reference/Item%20List.txt) | Complete item catalog: materials, food, furniture, outdoor, utilities, nature, buildings, blocks, kits |
| [Items by Favorite](reference/Items%20By%20Favorite.md) | 43 favorite categories with item lists for furnishing houses |
| [Habitats](reference/Habitats.md) | 209 regular + 3 event habitats with descriptions |
| [Locations](reference/Locations.md) | 6 area overviews with available materials and blocks |
| [Specialties](reference/Specialties.txt) | 31 Pokemon specialties reference |

---

## Tools

Scraping utilities for pulling data from the Pokopia wiki.

| File | Description |
|------|-------------|
| [pokopia scraper.py](tools/pokopia%20scraper.py) | Web scraper for Pokemon data |
| [pokopia_urls.txt](tools/pokopia_urls.txt) | URL list for scraping targets |
| [available pokemon.html](tools/available%20pokemon.html) | Cached HTML source |
| [bulbasaur.html](tools/bulbasaur.html) | Cached HTML source (example page) |

---

## Key Mechanics

- **Comfy Level** — Each Pokemon's happiness (Iffy > Average > Nice > Great > Awesome) based on habitat match + favorites
- **Environment Level** — Per-area progression (1–10) driven by aggregate Comfy Levels; unlocks shops, challenges, gifts
- **House Rules** — Max 10x10 blocks, 3+ unique furniture, up to 4 Pokemon per house
- **Map Height** — 127 blocks vertical across all areas
- **Habitat Types** — Bright, Cool, Dark, Dry, Humid, Warm — never cross habitat lines in housing

---

## Credits

Huge thanks to [Serebii](https://www.serebii.net/) for being such an incredible general Pokémon reference over the years.

Pokopia-specific data used in this project is scraped and compiled from Serebii.
The housing group assignments and planning structure are my own original work.
