"""Update index.html in place by swapping its embedded JSON data payload.

Lives in: Working Folder/Cache and Tools/
Reads:    extracted_data/g3g7_data.json   (produced by build_demographics_dashboard.py)
Writes:   REPO_ROOT/index.html             (only the <script id="data-payload"> block changes)

Run after build_demographics_dashboard.py. The dashboard's CSS, JS, slicer defaults,
and surrounding markup are preserved verbatim — only the inner contents of the
<script id="data-payload" type="application/json">...</script> element get replaced.
"""
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import DASHBOARD_JSON, DASHBOARD_HTML

PAYLOAD_RE = re.compile(
    r'(<script id="data-payload" type="application/json">)(.*?)(</script>)',
    re.DOTALL,
)


def main() -> int:
    if not os.path.exists(DASHBOARD_JSON):
        print(f"ERROR: dashboard JSON not found at {DASHBOARD_JSON}", file=sys.stderr)
        print("Run build_demographics_dashboard.py first.", file=sys.stderr)
        return 1
    if not os.path.exists(DASHBOARD_HTML):
        print(f"ERROR: index.html not found at {DASHBOARD_HTML}", file=sys.stderr)
        return 1

    with open(DASHBOARD_JSON, 'r', encoding='utf-8') as f:
        new_json = f.read().strip()
    with open(DASHBOARD_HTML, 'r', encoding='utf-8') as f:
        html = f.read()

    matches = PAYLOAD_RE.findall(html)
    if len(matches) != 1:
        print(
            f"ERROR: expected exactly one <script id=\"data-payload\"> block, "
            f"found {len(matches)} in {DASHBOARD_HTML}",
            file=sys.stderr,
        )
        return 2

    old_inner = matches[0][1]
    if old_inner == new_json:
        print(f"index.html payload already up to date — no change ({len(new_json):,} bytes).")
        return 0

    new_html = PAYLOAD_RE.sub(lambda m: m.group(1) + new_json + m.group(3), html, count=1)
    with open(DASHBOARD_HTML, 'w', encoding='utf-8') as f:
        f.write(new_html)

    print(
        f"index.html payload updated: {len(old_inner):,} → {len(new_json):,} bytes "
        f"({DASHBOARD_HTML})"
    )
    return 0


if __name__ == '__main__':
    sys.exit(main())
