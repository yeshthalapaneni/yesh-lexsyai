from typing import List
import re
from docxtemplater import Docxtemplater
from pizzip import PizZip
from .models import Placeholder




def _fill_in_xml(xml: str, placeholders: List[Placeholder]) -> str:
out = xml
def esc_xml(s: str) -> str:
return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


for p in placeholders:
val = esc_xml(p.value or "")
dn = re.escape(p.display_name)
patterns = [
re.compile(rf"\{{\{{\s*{p.name}\s*\}}\}}"),
re.compile(rf"\{{\s*{p.name}\s*\}}"),
re.compile(rf"\[\s*{dn}\s*\]"),
re.compile(rf"<\s*{dn}\s*>"),
]
for rx in patterns:
out = rx.sub(val, out)
return out




def fill_docx(original: bytes, placeholders: List[Placeholder]) -> bytes:
"""Try docxtemplater; fallback to raw XML replacement in document.xml."""
try:
zip1 = PizZip(original)
doc = Docxtemplater(zip1, {"paragraphLoop": True, "linebreaks": True})
data = {p.name: (p.value or "") for p in placeholders}
doc.render(data)
return doc.getZip().generate(type="nodebuffer", compression="DEFLATE")
except Exception:
zip2 = PizZip(original)
xml = zip2.file("word/document.xml").as_text()
filled = _fill_in_xml(xml, placeholders)
zip2.file("word/document.xml", filled)
return zip2.generate(type="nodebuffer", compression="DEFLATE")
