# Meow Burger v1.6.4 — web builds

Built from `main` with `python3 src/build.py`.

- `index.html`: one self-contained page (all art inlined) for testing on a phone or desktop browser. Ads are simulated test ads; HS SDK is not used.
- `minis/`: the H5 (web) TikTok Minis variant with the TikTok UI pack. The production upload is the native package on the `release/tiktok-native-*` branches.

To serve it with GitHub Pages: Settings → Pages → Deploy from branch → `web-build` / root. The game is then at `https://ybdstudio.github.io/meowburger/`.
