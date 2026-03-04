from pydantic import BaseModel
from typing import List


class PageIndexNode(BaseModel):
    title: str
    page_start: int
    page_end: int
    key_entities: List[str]
    summary: str
    data_types_present: List[str]
    children: List["PageIndexNode"] = []


PageIndexNode.update_forward_refs()
