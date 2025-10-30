import re
from typing import List, Tuple
from .models import Placeholder


SLUG_CHARS = re.compile(r"[^A-Za-z0-9]+")


def to_slug(s: str) -> str:
s = s.strip()
s = SLUG_CHARS.sub("_", s)
s = s.strip("_")
return s.lower()


# Patterns to capture placeholders in various legal templates
PATTERNS = [
re.compile(r"\{\{([^}]+)\}\}"), # {{company_name}}
re.compile(r"\{([A-Za-z0-9_ ]+)\}"), # {company name}
re.compile(r"\[([^\]]+)\]"), # [Company Name]
re.compile(r"<([^>]+)>") # <Company Name>
]


def extract_placeholders(text: str) -> Tuple[List[Placeholder], List[str]]:
seen = set()
placeholders: List[Placeholder] = []
matched_raw: List[str] = []


for rx in PATTERNS:
for m in rx.finditer(text):
raw = m.group(1).strip()
name = to_slug(raw)
if name not in seen and len(name) > 0:
seen.add(name)
placeholders.append(Placeholder(
id=f"ph-{len(placeholders)+1}",
name=name,
display_name=raw,
status="pending",
))
matched_raw.append(raw)


return placeholders, matched_raw




def naive_highlight(text: str, placeholders: List[Placeholder]) -> str:
"""Return a simple HTML with <mark> around placeholders for preview.
We escape HTML and then mark variants. This is *naive* and for demo only.
"""
def esc(s: str) -> str:
return (s.replace("&", "&amp;")
.replace("<", "&lt;")
.replace(">", "&gt;")
.replace('"', "&quot;")
.replace("'", "&#39;"))


safe = esc(text)
# highlight most specific (display_name) forms
for ph in placeholders:
dn = re.escape(ph.display_name)
variants = [
rf"\{{\{{\s*{ph.name}\s*\}}\}}",
rf"\{{\s*{ph.name}\s*\}}",
rf"\[\s*{dn}\s*\]",
rf"<\s*{dn}\s*>",
]
for v in variants:
safe = re.sub(v, rf"<mark data-ph='{ph.id}'>\g<0></mark>", safe)
return safe
