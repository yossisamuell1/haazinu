#!/bin/sh
# Full modesty screen over data/art.json: fetch thumbnails, NudeNet, CLIP zero-shot, scene blacklist.
set -e
cd "$(dirname "$0")/.."
echo "== NudeNet + thumbnail fetch"
python3 scripts/screen_art.py --in data/art.json 2>&1 | grep -vE 'WARN|onnx' | tail -3
echo "== CLIP"
python3 scripts/clip_screen.py --threshold 0.15 --apply 2>&1 | grep -vE 'Warning|WARNING' | grep -E '^(scored|applied)'
echo "== scene blacklist"
python3 scripts/blacklist_art.py
V=$(date +%Y%m%d%H%M)
sed -i '' "s#const DATA_V = \"[a-z0-9]*\"#const DATA_V = \"$V\"#" app.js
python3 -c "import json;d=json.load(open('data/art.json'));print('FINAL',d['meta']['count'],'artworks')"
