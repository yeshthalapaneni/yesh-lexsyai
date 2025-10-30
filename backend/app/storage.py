from typing import Dict
from .models import Placeholder


# In-memory, enough for this assignment
SESSIONS: Dict[str, dict] = {}
# session dict fields: {"filename": str, "doc_bytes": bytes, "placeholders": List[Placeholder]}
