"""Guard: the project keeps one report document. Fails if any tracked .docx is outside the allowlist.
Allowed: the report itself (report/inter-trade-report.docx) and the four source workbooks in sources/docx/ (inputs, not outputs).
Run from the repository root:  python -I -X utf8 scripts/check_single_docx.py
Used by scripts/save.ps1 before every commit and by .github/workflows/single-docx.yml on every push and pull request.
"""
import subprocess
import sys

ALLOWED_PREFIXES = ('sources/docx/',)
ALLOWED_EXACT = {'report/inter-trade-report.docx'}


def tracked_docx():
    out = subprocess.run(['git', 'ls-files', '*.docx'], capture_output=True, text=True, check=True).stdout
    return [line.strip() for line in out.splitlines() if line.strip()]


def main():
    bad = [f for f in tracked_docx() if f not in ALLOWED_EXACT and not f.startswith(ALLOWED_PREFIXES)]
    if bad:
        print('Refused: extra .docx files are tracked. Keep only report/inter-trade-report.docx:')
        for f in bad:
            print('  ' + f)
        return 1
    print('ok: one report document (report/inter-trade-report.docx)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
