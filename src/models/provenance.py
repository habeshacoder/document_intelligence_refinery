from pydantic import BaseModel
from typing import Tuple

BBox = Tuple[float, float, float, float]


class ProvenanceEntry(BaseModel):
    document_name: str
    page_number: int
    bbox: BBox
    content_hash: str
