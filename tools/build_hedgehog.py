"""Builds src/16_more_sprites.js from the HedgeBurger character pack (HedgeBurger_character_assets_v1.zip).

usage: python3 tools/build_hedgehog.py <path to the extracted HedgeBurger_assets_v1 folder>

Character reskin only: every role keeps its existing MORE_SPRITES key, frame names and canvas sizes; only the
pictures and the anchor data that depend on the pictures change. The 72 female-player frames are registered as
the extra set `player_female` (no entity uses it; the player stays `chef`).

Per frame:
  src     the runtime PNG from the role folder (WebP, lossless alpha), never previews / source sheets / designs
  w,h     PNG size (must equal manifest.json and source_inventory.json)
  ax,ay   the supplied foot pivot (manifest.json runtime_frames[].pivot_px)
  s       world scale (uniform: nothing is stretched). Some runtime PNGs were shrunk to fit their original
          canvas, so each frame is first evened out with the normalized atlas in spritesheets/ (atlas height /
          runtime height, relative to its group). idle / sit / tablet groups: one group scale so the group's median
          drawn height equals the cat art it replaces (same apparent world height). walk / carry-walk: the atlas
          evens out the 4 frames of a direction, and each direction's head is matched to the idle of the same
          direction (the atlas rows of different directions are not drawn at one size).
  legY    int(h*.84), as before (leg strip for stepping on idle art, seated leg fold)
  tray    carry frames only: where the hands are, so the game's separate tray + food stack sits in the empty
          hands. One hand position per direction (median over the 4 frames, in world units) -> no stack jitter.
"""
import sys, os, io, re, json, base64
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_JS = os.path.join(ROOT, 'src', '16_more_sprites.js')

# game set key -> pack folder (CHARACTER MAPPING)
ROLES = {'chef': '01_player_chef', 'cashier': '02_cashier', 'waiter': '03_runner_food_and_kitchen',
         'cleaner': '04_cleaner', 'manager': '05_manager', 'cat01': '06_customer_1', 'cat02': '07_customer_2',
         'cat03': '08_customer_3', 'cat04': '09_customer_4_purple_dress', 'vip01': '10_vip_1', 'vip02': '11_vip_2',
         'player_female': '13_player_female'}
# folder -> normalized atlases holding its frames (only used for the per-frame scale correction)
ATLASES = {'01_player_chef': ['male_idle', 'male_walk', 'male_carry'],
           '13_player_female': ['female_idle', 'female_walk', 'female_carry'],
           '02_cashier': ['cashier'], '03_runner_food_and_kitchen': ['runner'], '04_cleaner': ['cleaner'],
           '05_manager': ['manager'], '06_customer_1': ['customer_1'], '07_customer_2': ['customer_2'],
           '08_customer_3': ['customer_3'], '09_customer_4_purple_dress': ['customer_4'],
           '10_vip_1': ['vip_1'], '11_vip_2': ['vip_2']}
DIRS = [0, 315, 270, 225, 180, 135, 90, 45]   # pack order: front, front-right, right, back-right, back, back-left, left, front-left
# Values of the cat art this pack replaces (Meow Burger v1.6.4 src/16_more_sprites.js), per set and pose group:
# [scale s, median drawn height = alpha height * s]. Kept so the hedgehogs stand exactly as tall as the cats did.
CAT = {'chef': {'idle': [0.7697, 172.4], 'walk': [1.0229, 167.2], 'cwalk': [0.9896, 166.3]},
       'cashier': {'idle': [0.7348, 168.3], 'walk': [0.7127, 163.9]},
       'waiter': {'idle': [0.8025, 184.6], 'walk': [0.7784, 179.0]},
       'cleaner': {'idle': [0.7348, 168.3], 'walk': [0.7112, 163.6]},
       'manager': {'idle': [0.6656, 153.1], 'walk': [0.6456, 148.5], 'tablet': [0.6744, 154.4]},
       'cat01': {'idle': [0.73, 167.9], 'walk': [0.7081, 162.9], 'sit': [0.7094, 163.2], 'eat': [0.581, 133.0]},
       'cat02': {'idle': [0.6735, 154.9], 'walk': [0.6547, 150.3], 'sit_eat_seat': [0.6501, 148.9]},
       'cat03': {'idle': [0.6321, 144.8], 'walk': [0.6132, 141.0], 'sit_eat_seat': [0.6391, 147.0]},
       'cat04': {'idle': [0.6368, 146.5], 'walk': [0.6231, 142.1], 'sit_eat_seat': [0.6276, 143.1]},
       'vip01': {'idle': [0.6695, 154.0], 'walk': [0.6523, 149.4], 'sit_eat_seat': [0.6938, 159.2]},
       'vip02': {'idle': [0.7132, 164.0], 'walk': [0.6918, 159.1], 'sit_eat_seat': [0.6156, 141.0]}}


def group(name):
    for g in ('cwalk', 'walk', 'idle', 'sit_eat_seat', 'sit', 'eat', 'tablet'):
        if name.startswith(g): return g
    raise ValueError(name)


def frames_for(key, folder, files):
    """Existing frame names of a set, in a stable order (directions in pack order)."""
    names = {f[:-4] for f in files if f.endswith('.png')}
    order = ['idle_%d' % d for d in DIRS]
    for pre in ('walk', 'cwalk'):
        order += ['%s%d_%d' % (pre, i, d) for d in DIRS for i in range(1, 5)]
    order += sorted(n for n in names if not re.match(r'(idle|c?walk\d)_', n))
    return [n for n in order if n in names]


def alpha_h(a):
    ys = np.nonzero((a[..., 3] > 128).any(1))[0]
    return int(ys.max() - ys.min() + 1)


def headw(a, lo=.12, hi=.40):
    """Median width of the head + quills band (12–40 % down the figure), in px."""
    m = a[..., 3] > 128; ys = np.nonzero(m.any(1))[0]; t = ys.min(); H = ys.max() - t + 1; ws = []
    for y in range(t + int(H * lo), t + int(H * hi)):
        xs = np.nonzero(m[y])[0]; ws.append(xs.max() - xs.min() + 1 if len(xs) else 0)
    return float(np.median(ws))


def enc(im):
    b = io.BytesIO(); im.save(b, 'WEBP', quality=92, method=6, alpha_quality=100)
    return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()


def hands(a):
    """Centre of the empty paws (paw colour, below the face) in px, or None."""
    A = a.astype(int); h = A.shape[0]; r, g, b, al = A[..., 0], A[..., 1], A[..., 2], A[..., 3]
    m = (al > 200) & (r > 232) & (g > 150) & (g < 205) & (b > 75) & (b < 140)
    m[:int(h * .55)] = False; m[int(h * .86):] = False
    lab, n = ndimage.label(m)
    if n == 0: return None
    sz = ndimage.sum(m, lab, range(1, n + 1)); keep = [i + 1 for i in np.argsort(-sz)[:2] if sz[i] >= 25]
    if not keep: return None
    ys, xs = np.nonzero(np.isin(lab, keep))
    return float(xs.mean()), float(np.percentile(ys, 30))


def main(PACK):
    man = {f['path']: f for f in json.load(open(os.path.join(PACK, 'manifest.json')))['runtime_frames']}
    inv = {f['path']: f for f in json.load(open(os.path.join(PACK, 'source_inventory.json')))}
    report = {'frames': 0, 'errors': [], 'scale_fix': {}}
    # atlas cells: drawn height of each frame at the shared normalized scale
    atlas_h = {}
    for folder, sheets in ATLASES.items():
        for sh in sheets:
            J = json.load(open(os.path.join(PACK, 'spritesheets', sh + '.json')))
            img = np.array(Image.open(os.path.join(PACK, 'spritesheets', J['image'])).convert('RGBA'))
            for f in J['frames']:
                x, y, w, h = f['rect']; atlas_h[(folder, f['name'])] = alpha_h(img[y:y + h, x:x + w])
    OUT, IMG = {}, {}
    for key, folder in ROLES.items():
        files = os.listdir(os.path.join(PACK, folder)); OUT[key] = {}
        for name in frames_for(key, folder, files):
            rel = folder + '/' + name + '.png'
            im = Image.open(os.path.join(PACK, rel))
            if im.mode != 'RGBA': report['errors'].append(rel + ' not RGBA'); im = im.convert('RGBA')
            mf = man.get(rel)
            if not mf: report['errors'].append(rel + ' missing from manifest'); continue
            if list(im.size) != mf['size']: report['errors'].append('%s size %s != manifest %s' % (rel, im.size, mf['size']))
            if not folder.startswith('13_') and (rel not in inv or list(im.size) != inv[rel]['size']):
                report['errors'].append(rel + ' does not match source_inventory')
            a = np.array(im); IMG[(key, name)] = a
            w, h = im.size; px, py = mf['pivot_px']
            OUT[key][name] = {'w': w, 'h': h, 'ax': px, 'ay': py, 's': 0, 'legY': int(h * .84), 'src': enc(im)}
            report['frames'] += 1
    # scales: per-frame atlas correction, then one group scale preserving the cat's drawn height
    for key, fr in OUT.items():
        folder = ROLES[key]; base = 'chef' if key == 'player_female' else key
        gs = {}
        for n in fr: gs.setdefault(group(n), []).append(n)
        for g, names in gs.items():
            ratio = {n: atlas_h[(folder, n)] / alpha_h(IMG[(key, n)]) for n in names}
            if key == 'player_female':   # same atlas scale as the male player -> same size as him
                ref = float(np.median([atlas_h[('01_player_chef', n)] / alpha_h(IMG[('chef', n)]) for n in OUT['chef'] if group(n) == g]))
            else:
                ref = float(np.median(list(ratio.values())))
            corr = {n: ratio[n] / ref for n in names}
            if key == 'player_female':
                s_g = OUT['chef'][next(n for n in OUT['chef'] if group(n) == g)]['s_g']
            else:
                drawn = float(np.median([alpha_h(IMG[(key, n)]) * corr[n] for n in names]))
                s_g = CAT[key][g][1] / drawn
            for n in names:
                OUT[key][n]['s'] = round(s_g * corr[n], 4); OUT[key][n]['s_g'] = s_g
        # walk / carry-walk: the atlas rows of different directions are not drawn at one size, so the atlas only
        # evens out the 4 frames of one direction; each direction is then sized so its head matches the idle of
        # the same direction (no size jump between standing and walking, or between directions).
        for g in ('walk', 'cwalk'):
            for d in DIRS:
                names = [n for n in fr if group(n) == g and n.endswith('_%d' % d)]
                if not names: continue
                ratio = {n: atlas_h[(folder, n)] / alpha_h(IMG[(key, n)]) for n in names}
                ref = float(np.median(list(ratio.values())))
                corr = {n: ratio[n] / ref for n in names}
                mi = OUT[key]['idle_%d' % d]
                k = headw(IMG[(key, 'idle_%d' % d)]) * mi['s'] / float(np.median([headw(IMG[(key, n)]) * corr[n] for n in names]))
                for n in names: OUT[key][n]['s'] = round(k * corr[n], 4)
        for n, m in fr.items():
            f = m['s'] / m['s_g']
            if abs(f - 1) > .03: report['scale_fix'][key + '/' + n] = round(f, 3)
    # carry: one hand point per direction, in world units from the feet
    for key in ('chef', 'player_female'):
        for d in DIRS:
            names = ['cwalk%d_%d' % (i, d) for i in range(1, 5)]
            off = []
            for n in names:
                m = OUT[key][n]; hp = hands(IMG[(key, n)])
                if hp: off.append(((hp[0] - m['ax']) * m['s'], (hp[1] - m['ay']) * m['s']))
            if not off: report['errors'].append('%s cwalk %d: hands not found' % (key, d)); continue
            dx, dy = float(np.median([o[0] for o in off])), float(np.median([o[1] for o in off]))
            for n in names:
                m = OUT[key][n]
                m['tray'] = [round((m['ax'] + dx / m['s']) / m['w'], 3), round((m['ay'] + dy / m['s']) / m['h'], 3)]
    for fr in OUT.values():
        for m in fr.values(): m.pop('s_g', None)
    # keep each frame's keys in the old order
    order = ['w', 'h', 'ax', 'ay', 's', 'legY', 'tray', 'src']
    OUT = {k: {n: {q: m[q] for q in order if q in m} for n, m in fr.items()} for k, fr in OUT.items()}
    if report['errors']:
        print(json.dumps(report, indent=1)); sys.exit('errors: nothing written')
    js = ('/* 16_more_sprites.js — HedgeBurger character art (HedgeBurger_character_assets_v1). '
          'AUTO-GENERATED by tools/build_hedgehog.py */\nconst MORE_SPRITES=' + json.dumps(OUT, separators=(',', ':')) + ';\n')
    open(OUT_JS, 'w').write(js)
    report['sets'] = {k: len(v) for k, v in OUT.items()}; report['kb'] = len(js) // 1024
    print(json.dumps(report, indent=1))


if __name__ == '__main__':
    if len(sys.argv) != 2: sys.exit(__doc__)
    main(sys.argv[1])
