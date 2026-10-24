# Meow Burger v1.6.4 — TikTok Minis upload package

Built from `main` (v1.6.4) with the real App ID and ad unit IDs.

**Before uploading:** put the HS SDK key (`sk_live_…`) in `native/meow-config.js` (`hsSdkKey`). It is left blank here because GitHub push protection blocks keys that start with `sk_live_` (it mistakes them for Stripe keys). The ready-to-upload zip with the key is delivered outside the repo.

- `native/`: the package to upload. Zip the **contents** of this folder so `game.json` is at the zip root, or run `ttmg dev` inside it.
- `native.hs-dashboard.json`: paste its `iaa_config` into HS → Ads Config → Edit raw JSON. It is not part of the upload.

Checks: `tests/qa_native.js` 44/44, `hs-check` 0 fail (7 warnings: placement labels with capitals, matching the HS dashboard).

The TikTok Client Secret is never in this repo.
