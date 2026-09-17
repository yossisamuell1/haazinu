#!/bin/sh
# Screen the harvested artwork for nudity, install it as data/art.json, and bump the app's data version.
set -e
cd "$(dirname "$0")/.."
python3 scripts/screen_art.py --in .work/art/art_raw.json "$@"
cp .work/art/art_raw.json data/art.json
V=$(date +%Y%m%d%H%M)
sed -i '' "s#const DATA_V = \"[a-z0-9]*\"#const DATA_V = \"$V\"#" app.js
python3 -c "import json;d=json.load(open('data/art.json'));print('installed',d['meta']['count'],'artworks')"
