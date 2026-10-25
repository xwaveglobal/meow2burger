# Meow Burger — changelog

Engine history before Meow Burger (Meow Pizza v4.x) is in `docs/pizza-legacy/CHANGELOG_pizza.md`.

## Unreleased — Hedge Burger v1.2 corrections
- Public name is two words, "Hedge Burger" (page title, popups, share title, stage/spot names, project.config.json, package comments).
- Corrected art from the v1.2 pack: loading title reads "Hedge Burger" (normal g), logo, Home/Profile guide images with the spaced name, revisit coin banner with H stamps (its v1.1 "cat-free" label was wrong).
- Remaining cat/meow wording: boost "Meow Rush"/"MEOW RUSH" → "Hedge Burger"/"HEDGE BURGER" (label sized to fit its button), "Hedge cashier"/"Hedge cleaner" spots, "Hire a Hedge cashier/cleaner" tasks, loading "Calling the Hedge crew…" and "Ready! Hedge!".
- Kept for HS / compatibility: ad placement label, reward key and item name "Meow Rush" (must match the HS dashboard), save key `meowburger.v3`, ids `meow_rush`, `cat01…`, file names `meow-config.js`, `cat_cola.png`.

## HedgeBurger v1.1 asset update
- Left walk: the 10 non-player roles walk to screen-left with their own drawn frames (`walk1–4_90`), no mirroring; sized to their right walk.
- T-side chair: the 6 customers / VIPs sit there with the drawn front-left set (`sit_eat_left1` waiting, 1–4 while eating), no mirroring. L-side chair unchanged.
- Branding: display name HedgeBurger (page title, popups, share title, stage/spot names, project.config.json projectname); drink shown as Hedge Cola (item id `drink` unchanged). Save key, ad labels and file names unchanged.
- Brand art from the pack: loading art, app icons, loading-bar thumb, Launch Reward button, Home / Revisit / Share popup art; trash bin, fridge, 3 storage shelves, pickup counter, cola cup, burger box and ingredient crate with hedgehog logos (`tools/apply_brand_v11.py`).
- Code-drawn marks: hedgehog emblem (`branding/hedgehog_mark.png`, embedded as `ENV_ART.hedgemark`) on the staff door and the PICK UP sign; queue-slot floor marks are a white hedgehog stamp instead of paw prints (same place, size and opacity).

## HedgeBurger character reskin
- Every character (player, cashier, food/kitchen runner, cleaner, manager, customers 1–4, VIP 1–2) uses the hedgehog art from `HedgeBurger_character_assets_v1.zip`. Gameplay, timings, map, UI and save data unchanged.
- `src/16_more_sprites.js` is now built by `tools/build_hedgehog.py` from the pack: same set keys, frame names and canvas sizes; foot pivots from the pack manifest; scales keep each character's apparent height.
- The 72 female-player frames are registered as the set `player_female` (not used by any entity; the player stays male).
- Renderer: carry art has empty hands, so the tray is drawn under the carried food; the player's front/back walk and carry-walk use the drawn frames; idle direction substitutes made for the old cat cuts are gone.

## v1.6.4 — TikTok native release
- The 3 TikTok gift buttons (Revisit, Share, Launch/Home) show on the play screen from the first frame after loading, on web and native.
- Auto play turned off (`CFG.autoPlay:false`): AUTO button hidden, a saved auto setting is ignored. Set it to `true` to bring it back.
- HS SDK:
  - `HSGame.start` is always called; with placeholder credentials login fails, and ads, missions and cloud stay off while the game keeps playing.
  - Cloud save: `HSGame.save(progress)` after every save (debounced). `onLoad` keeps the further progress (higher task, then more coins).
  - Gift amounts in popups come from `HSGame.rewards()` (dashboard), with the old numbers as offline defaults.
  - Every placement is logged with `canShowAd` after start.
- Build: credentials and the dashboard placements export come from `src/native/hs-config.json`. The build fills in the appid, `meow-config.js` and the ad unit IDs, and warns when game labels and dashboard labels differ.
- Placement labels match HS: Double Task Bonus, Buying Pad, Meow Rush, VIP tip, Coin Purchase, Grand Opening, Grill Break.
- Tests: qa_native 44/44, hs-check 0 fail (7 capital-letter label warnings).

## v1.6.3 — Native package with placeholders
- First TikTok Minis native package for Meow Burger, with blank App ID, SDK key and ad unit IDs.
- Credentials moved out of the HS bridge into `meow-config.js` next to `game.js`. Meow Pizza credentials removed.
- Sprites under `art/` are converted from WebP to PNG for the native runtime.
- Visual fixes: player cap tip restored in walk and carry frames, walk cycle anchored at the feet, code-drawn planter, loading screen uses the full art with the loading bar drawn live.

## v1.3 – v1.6 — Layout and art passes
- Kitchen stations redrawn in code against the walls (`src/26_stations_code.js`), storage rack and tables drawn in code.
- Seated customers drawn behind their tables; VIP rug on the floor; balloon arches grounded; trees behind the walls painted before the walls.
- Patio expansion and post-grand-opening goals; navigation grid enlarged for the patio.
- Overhead icons for waiting, angry, cash, trash and sleeping.
- Auto play with ×2 speed (now off by default, see v1.6.4).
- Grill Break interstitial every 45 s of play, starting from the first take-food task.

## v1.2 — First web test build
- Meow Burger reskin of the Meow Pizza engine: chicken is the first station; burger, fries, salad, drinks, chicken burger and deluxe burger follow.
- Approved P1 environment, asset-kit characters (cashier, food runner, cleaner, manager, customers, VIP) and the user's player sheets.
- Full bot run 35:13 with no customers lost.
