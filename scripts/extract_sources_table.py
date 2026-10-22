"""Build the A15 source table (tag -> title) from the workbook text dumps. Prints Markdown rows to stdout.

usage: python -I -X utf8 scripts/extract_sources_table.py > outline/_a15_workbook_sources.md
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
files = [
    os.path.join(ROOT, "sources", "text", "inter-trade-present-2-revised-research-brief.txt"),
    os.path.join(ROOT, "sources", "text", "inter-trade-present-base.txt"),
]
pat = re.compile(r"^\[((?:U|S|G)\d+)\]\s+(.+)$")
found = {}
for path in files:
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = pat.match(line.rstrip("\n"))
            if m and m.group(1) not in found:
                found[m.group(1)] = m.group(2).strip()


def key(t):
    return (t[0], int(t[1:]))


print("| Tag | Source |")
print("| --- | --- |")
for tag in sorted(found, key=key):
    title = found[tag].replace("|", "/")
    print("| %s | %s |" % (tag, title))
