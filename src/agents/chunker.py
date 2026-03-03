from typing import List
import hashlib

from src.models.extracted_document import ExtractedDocument
from src.models.ldu import LDU


class ChunkValidator:
    def validate(self, ldus: List[LDU]) -> None:
        # TODO: enforce all five chunking rules explicitly
        pass


class ChunkingEngine:
    def __init__(self):
        self.validator = ChunkValidator()

    def _hash(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def chunk(self, doc: ExtractedDocument) -> List[LDU]:
        ldus: list[LDU] = []

        for i, tb in enumerate(doc.text_blocks):
            chunk_id = f"{doc.doc_id}-p{tb.page}-b{i}"
            content = tb.text
            ldus.append(
                LDU(
                    doc_id=doc.doc_id,
                    chunk_id=chunk_id,
                    content=content,
                    chunk_type="paragraph",
                    page_refs=[tb.page],
                    bounding_box=tb.bbox,
                    parent_section="",
                    token_count=len(content.split()),
                    content_hash=self._hash(content),
                )
            )

        self.validator.validate(ldus)
        return ldus
