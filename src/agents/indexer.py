from typing import List

from src.models.ldu import LDU
from src.models.pageindex import PageIndexNode


class PageIndexBuilder:
    def build(self, doc_id: str, ldus: List[LDU]) -> PageIndexNode:
        # Simple single-node index; replace with hierarchical logic + LLM summaries
        pages = sorted({p for l in ldus for p in l.page_refs})
        summary = f"Document {doc_id} with {len(ldus)} chunks."
        root = PageIndexNode(
            title=doc_id,
            page_start=pages[0] if pages else 1,
            page_end=pages[-1] if pages else 1,
            key_entities=[],
            summary=summary,
            data_types_present=["text"],
            children=[],
        )
        return root
