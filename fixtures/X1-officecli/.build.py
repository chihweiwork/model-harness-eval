#!/usr/bin/env python3
"""Build report.docx (OFFX container) from plaintext. Run once at fixture setup.

The runner excludes dotfiles when copying fixtures, so this file never
reaches the model's working directory.
"""

import base64
from pathlib import Path

TEXT = (
    "The quarterly report shows steady growth across all regions. "
    "Sales increased by twelve percent compared to last year. "
    "Customer satisfaction remains high according to recent surveys. "
    "The engineering team shipped four major features this quarter. "
    "Next quarter we plan to expand into two new markets."
)

# sanity: word count must be 45 (the benchmark's expected answer)
assert len(TEXT.split()) == 45, len(TEXT.split())

payload = base64.b64encode(TEXT.encode()).decode()
doc = "\n".join(
    ["OFFX1", "title: Q3 Business Report", "author: bench", "---", payload, ""]
)
out = Path(__file__).parent / "report.docx"
out.write_text(doc)
print(f"wrote {out} ({len(TEXT.split())} words)")
