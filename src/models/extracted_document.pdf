from pydantic import BaseModel
from typing import List, Optional, Tuple

BBox = Tuple[float, float, float, float]


class TextBlock(BaseModel):
    page: int
    bbox: BBox
    text: str


class TableCell(BaseModel):
    row: int
    col: int
    text: str
    bbox: BBox


class Table(BaseModel):
    page: int
    bbox: BBox
    headers: List[str]
    rows: List[List[TableCell]]


class Figure(BaseModel):
    page: int
    bbox: BBox
    caption: Optional[str] = None


class ExtractedDocument(BaseModel):
    doc_id: str
    text_blocks: List[TextBlock]
    tables: List[Table]
    figures: List[Figure]
