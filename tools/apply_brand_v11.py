"""Applies the Hedge Burger brand images (HedgeBurger_update_v1.1.zip / _v1_1 full pack / HedgeBurger_update_v1.2.zip).

usage: python3 tools/apply_brand_v11.py <path to the extracted HedgeBurger_assets_v1 folder (v1.1 or v1.2)>

Reads patch_manifest_v1.2.json when present (it supersedes v1.1: corrected loading wordmark, logo, guide images and
the revisit coin banner, whose v1.1 "cat-free" label was wrong), else patch_manifest_v1.1.json.
Replaces only the images the manifest lists in "ui_and_brand_assets", keeping every size; each file must match the
manifest's sha256 when it gives one:
  04_tiktok_ui/*      -> assets/minis/<same name>     (loading art, icons, popup art, buttons, loading-bar thumb)
  02_stations_props/* -> src/18_env_art.js ENV_ART     (pack file names are the original kit's; the game keys differ)
  03_food/*           -> src/17_pizza_art.js FOOD_ART
  branding/*          -> assets/branding/<same name>;  hedgehog_mark.png is also embedded as ENV_ART.hedgemark
                         (drawn on the door emblem and the queue floor marks)
The pack file -> game key pairs below were matched by size (identical) and picture. Only the matching data URIs
are swapped; nothing else in the generated modules changes.
"""
import sys, os, io, re, json, base64, shutil, hashlib
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV = {'02_stations_props/trash_bin.png': 'bin', '02_stations_props/storage_shelf_2.png': 'shelf1',
       '02_stations_props/storage_shelf_3.png': 'shelf2', '02_stations_props/storage_shelf_4.png': 'shelf3',
       '02_stations_props/fridge.png': 'fridge', '02_stations_props/counter_center.png': 'ctrC'}
FOOD = {'03_food/cat_cola.png': 'drink', '03_food/ingredients.png': 'ing', '03_food/chicken_box.png': 'box'}


def enc(path):
    b = io.BytesIO(); Image.open(path).convert('RGBA').save(b, 'WEBP', quality=92, method=6, alpha_quality=100)
    return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()


def load_obj(text, name):
    """The JSON object literal assigned to `const NAME=` in a generated module."""
    i = text.index('const %s=' % name) + len('const %s=' % name)
    obj, end = json.JSONDecoder().raw_decode(text, i)
    return obj, i, end


def main(PACK):
    mp = next(os.path.join(PACK, n) for n in ('patch_manifest_v1.2.json', 'patch_manifest_v1.1.json') if os.path.exists(os.path.join(PACK, n)))
    man = json.load(open(mp)); print('manifest', os.path.basename(mp))
    listed = {a['path']: a for a in man['ui_and_brand_assets']}
    log = []
    for p in list(ENV) + list(FOOD):
        assert p in listed, p + ' not in patch manifest'
    # ---- generated modules: swap the matching data URIs
    for fn, var, table in (('18_env_art.js', 'ENV_ART', ENV), ('17_pizza_art.js', 'FOOD_ART', FOOD)):
        path = os.path.join(ROOT, 'src', fn); text = open(path).read(); obj, _, _ = load_obj(text, var)
        for p, key in table.items():
            im = Image.open(os.path.join(PACK, p)); old = obj[key]
            old_src = old if isinstance(old, str) else old['src']
            ow, oh = Image.open(io.BytesIO(base64.b64decode(old_src.split(',', 1)[1]))).size
            assert im.size == (ow, oh), '%s %s != %s.%s %s' % (p, im.size, var, key, (ow, oh))
            assert text.count(old_src) == 1
            text = text.replace(old_src, enc(os.path.join(PACK, p))); log.append('%s -> %s.%s %dx%d' % (p, var, key, ow, oh))
        if var == 'ENV_ART':
            obj, i, end = load_obj(text, var)
            mark = os.path.join(PACK, 'branding', 'hedgehog_mark.png'); w, h = Image.open(mark).size
            entry = json.dumps({'src': enc(mark), 'w': w, 'h': h}, separators=(',', ':'))
            if 'hedgemark' in obj:
                text = text.replace(json.dumps(obj['hedgemark']['src']), json.dumps(enc(mark)))
            else:
                text = text[:end - 1] + ',"hedgemark":' + entry + text[end - 1:]
            log.append('branding/hedgehog_mark.png -> ENV_ART.hedgemark %dx%d' % (w, h))
        open(path, 'w').write(text)
    # ---- files: TikTok UI art and the brand originals
    for p, a in listed.items():
        src = os.path.join(PACK, p)
        if p.startswith('04_tiktok_ui/'):
            dst = os.path.join(ROOT, 'assets', 'minis', os.path.basename(p))
            assert Image.open(dst).size == Image.open(src).size, p
            if a.get('sha256'):   # file must be exactly the one the manifest describes
                assert hashlib.sha256(open(src, 'rb').read()).hexdigest() == a['sha256'], p
            same = open(src, 'rb').read() == open(dst, 'rb').read()
            if not same: shutil.copyfile(src, dst)
            log.append('%s -> assets/minis/%s%s' % (p, os.path.basename(p), ' (unchanged)' if same else ''))
        elif p.startswith('branding/'):
            os.makedirs(os.path.join(ROOT, 'assets', 'branding'), exist_ok=True)
            shutil.copyfile(src, os.path.join(ROOT, 'assets', 'branding', os.path.basename(p)))
            log.append('%s -> assets/branding/%s' % (p, os.path.basename(p)))
    print('\n'.join(log)); print(len(log), 'entries')


if __name__ == '__main__':
    if len(sys.argv) != 2: sys.exit(__doc__)
    main(sys.argv[1])
