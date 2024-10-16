from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class ProjSummary:
    utc_updated_timestamp: Optional[str] = ""


@dataclass
class Proj:
    id: str
    name: str
    tag: str
    utc_created_timestamp: str
    color: str
    is_pinned: str
    ql: str
    description: str
    user_id: str
    utc_updated_timestamp: str
    summary: ProjSummary

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Proj":
        obj = cls(**d)
        obj.summary = None

        summary = d.get("summary", None)
        if summary:
            obj.summary = ProjSummary(**summary)

        return obj
