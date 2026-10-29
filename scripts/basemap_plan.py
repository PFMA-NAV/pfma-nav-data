"""Plan a base-map run: map each requested country (ISO 3166-1 alpha-2) to its Geofabrik extract.

Writes plan.json ({"areas": [{"area": id, "countries": [...]}], "unavailable": [...]}) and, under
GitHub Actions, the job matrix to $GITHUB_OUTPUT. Countries that share one extract (Haiti and the
Dominican Republic, the GCC states...) are built once.

    python scripts/basemap_plan.py all|CL,AR
"""
import json
import os
import sys
import urllib.request

GEOFABRIK_INDEX = 'https://download.geofabrik.de/index-v1-nogeom.json'

# Extracts the index does not tag with the country code, or tags ambiguously.
OVERRIDES = {
    'BN': 'malaysia-singapore-brunei',
    'EH': 'morocco',
    'FK': 'falklands',
    'SA': 'gcc-states',
    'SG': 'malaysia-singapore-brunei',
    'VU': 'vanuatu',
    'XK': 'kosovo',
}


def main():
    wanted = sys.argv[1].strip() if len(sys.argv) > 1 else 'all'
    if wanted.lower() in ('', 'all'):
        with open('basemap-countries.txt', encoding='utf-8') as f:
            countries = [line.strip() for line in f if line.strip()]
    else:
        countries = [c.strip().upper() for c in wanted.split(',') if c.strip()]
    with urllib.request.urlopen(GEOFABRIK_INDEX, timeout=60) as r:
        index = json.load(r)
    by_code = {}
    for feature in index['features']:
        props = feature['properties']
        for code in props.get('iso3166-1:alpha2') or []:
            by_code.setdefault(code, []).append(props['id'])
    areas, unavailable = {}, []
    for code in countries:
        area = OVERRIDES.get(code)
        if area is None:
            found = by_code.get(code, [])
            area = found[0] if len(found) == 1 else None
        if area is None:
            unavailable.append(code)
            continue
        areas.setdefault(area, []).append(code)
    plan = {
        'areas': [{'area': a, 'countries': sorted(c)} for a, c in sorted(areas.items())],
        'unavailable': sorted(unavailable),
    }
    with open('plan.json', 'w', encoding='utf-8') as f:
        json.dump(plan, f, indent=1)
    print(f"{len(plan['areas'])} extracts for {len(countries) - len(unavailable)} countries; "
          f"unavailable: {' '.join(plan['unavailable']) or 'none'}")
    output = os.environ.get('GITHUB_OUTPUT')
    if output:
        with open(output, 'a', encoding='utf-8') as f:
            f.write('matrix=' + json.dumps({'include': plan['areas']}) + '\n')


if __name__ == '__main__':
    main()
