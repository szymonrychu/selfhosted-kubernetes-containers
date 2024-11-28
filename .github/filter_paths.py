#!/usr/bin/env python3

import json
import sys

def main():
    json_changed_files = sys.argv[1]
    changed_files = json.loads(json_changed_files)

    filtered_files = []
    for f in changed_files:
        if f.startswith('apps'):
          filtered_files.append(f.strip())

    print(f"changed_containers={filtered_files}")
    print(f"changed_containers={filtered_files}", file=sys.stderr)

if __name__ == '__main__':
    main()