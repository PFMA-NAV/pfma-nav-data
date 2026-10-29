"""Merge the per-extract results of a base-map run into basemap-index.json.

Each build job leaves results/<area>.json ({"area", "file", "sha256", "bytes", "countries"}). Extracts
built in this run point to its release; the others keep the entry of the previous index, so a run for
a few countries never drops the rest. Countries without any extract are listed as unavailable.

    python scripts/basemap_index.py <release tag> <results dir> <plan.json> [previous index]
"""
import datetime
import glob
import json
import os
import sys

LAYERS = ['landuse', 'water', 'waterway', 'transportation', 'place', 'mountain_peak', 'aeroway', 'aerodrome_label']


def main():
    tag, results_dir, plan_path = sys.argv[1:4]
    previous_path = sys.argv[4] if len(sys.argv) > 4 else None
    with open(plan_path, encoding='utf-8') as f:
        plan = json.load(f)
    previous = {}
    if previous_path and os.path.exists(previous_path):
        with open(previous_path, encoding='utf-8') as f:
            previous = json.load(f)
    areas = dict(previous.get('areas', {}))
    built = set()
    for path in sorted(glob.glob(os.path.join(results_dir, '**', '*.json'), recursive=True)):
        with open(path, encoding='utf-8') as f:
            r = json.load(f)
        areas[r['area']] = {
            'tag': tag,
            'file': r['file'],
            'sha256': r['sha256'],
            'bytes': r['bytes'],
            'countries': r['countries'],
        }
        built.add(r['area'])
    countries = {code: area for area, e in sorted(areas.items()) for code in e['countries']}
    with open('basemap-countries.txt', encoding='utf-8') as f:
        world = [line.strip() for line in f if line.strip()]
    failed = sorted({a['area'] for a in plan['areas']} - built)
    index = {
        'format': 1,
        'generated': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'source': 'OpenStreetMap (Geofabrik extracts) via Planetiler, OpenMapTiles schema',
        'license': 'Data ODbL 1.0 (OpenStreetMap); tile schema CC-BY 4.0 (OpenMapTiles)',
        'attribution': '© OpenMapTiles © OpenStreetMap contributors',
        'tiles': 'pmtiles',
        'maxzoom': 12,
        'layers': LAYERS,
        'areas': dict(sorted(areas.items())),
        'countries': dict(sorted(countries.items())),
        'unavailable': sorted(c for c in world if c not in countries),
    }
    with open('basemap-index.json', 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=1)
    print(f"built {len(built)} extracts in {tag}; index covers {len(countries)} countries; "
          f"failed: {' '.join(failed) or 'none'}")
    if failed:
        sys.exit(1)


if __name__ == '__main__':
    main()
