from pydantic import BaseModel
from typing import List, Literal, Tuple

BBox = Tuple[float, float, float, float]


class LDU(BaseModel):
    doc_id: str
    chunk_id: str
    content: str
    chunk_type: Literal["paragraph", "table", "figure", "list"]
    page_refs: List[int]
    bounding_box: BBox
    parent_section: str
    token_count: int
    content_hash: str
