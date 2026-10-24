# Meow Burger — art source

Source sheets that the art pipeline on `main` (`tools/*.py`) cuts sprites from. The generated sprite modules (`src/15–18_*.js`) are already committed on `main`, so you only need this branch to re-cut art.

- `burgerkit/`: the asset-kit sheets the tools use (cashier 016+002, food runner, staff, customers, VIP, stations, props, shelf 060…) plus the kit's manifest and art/animation guide.
- `work/`: approved P1 scene (`P1_env.png`, `env/p1_full.png`, `env/p1_empty.png`), cleaned environment atlases (`env/atlas.png`, `env/pickup.png`, `env/chicken19*.png`), player sheets with label pills erased (`P_walk.png`, `P_carry.png`, `P_idle*.png`) and the fixed sitting pose (`cat01_sit.png`).
- `tiktokui/`: TikTok UI pack (loading art, icon, share / revisit / launch popups and buttons).

## Re-cutting
The tools read these files from fixed paths. Check them out like this, then run the tools from a `main` checkout at `/home/claude/burger`:

```
/home/claude/src/burgerkit/   <- burgerkit/
/home/claude/work/            <- work/
```

```bash
python3 tools/build_chars.py    # -> src/16_more_sprites.js
python3 tools/build_env.py      # -> src/18_env_art.js
python3 tools/build_kit_art.py  # -> src/17_pizza_art.js
```
