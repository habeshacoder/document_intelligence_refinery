from typing import List, Tuple

from src.models.pageindex import PageIndexNode
from src.models.provenance import ProvenanceEntry
from src.models.ldu import LDU


class QueryAgent:
    def __init__(self, ldus: List[LDU], pageindex: PageIndexNode):
        self.ldus = ldus
        self.pageindex = pageindex

    def answer(self, question: str) -> Tuple[str, List[ProvenanceEntry]]:
        # TODO: plug in proper vector search + PageIndex navigation + SQL fact tables
        if not self.ldus:
            return "No data.", []

        best = self.ldus[0]
        answer = best.content[:300]
        prov = [
            ProvenanceEntry(
                document_name=best.doc_id,
                page_number=best.page_refs[0] if best.page_refs else 1,
                bbox=best.bounding_box,
                content_hash=best.content_hash,
            )
        ]
        return answer, prov
