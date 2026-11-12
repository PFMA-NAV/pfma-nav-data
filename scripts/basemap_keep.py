"""Print the base-map release tags that some published index may still point to, one per line.

A release named by the index just published, or by the one before it, can still be asked for by an app that
read either index; every other basemap-YYYYMMDD-HHMM release is superseded and can be removed. Prints nothing
when no index can be read, so the caller removes nothing.

    python scripts/basemap_keep.py <new index> [previous index]
"""
import json
import sys


def tags(path):
    try:
        with open(path, encoding='utf-8') as f:
            return {area['tag'] for area in json.load(f)['areas'].values()}
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return None


def main():
    current = tags(sys.argv[1])
    if not current:
        return
    keep = set(current)
    for path in sys.argv[2:]:
        keep |= tags(path) or set()
    print('\n'.join(sorted(keep)))


if __name__ == '__main__':
    main()
