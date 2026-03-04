from typing import List
import hashlib

from src.models.extracted_document import ExtractedDocument, Table
from src.models.ldu import LDU


class ChunkValidator:
    def validate(self, ldus: List[LDU]) -> None:
        # Basic checks; expand as needed
        # 1) no table chunks without headers
        for l in ldus:
            if l.chunk_type == "table" and "header:" not in l.content:
                raise ValueError("Table chunk without header in content.")
        # You can add more checks to reflect the constitution rules
        return


class ChunkingEngine:
    def __init__(self):
        self.validator = ChunkValidator()

    def _hash(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def _chunk_tables(self, doc: ExtractedDocument) -> List[LDU]:
        table_ldus: List[LDU] = []
        for idx, tbl in enumerate(doc.tables):
            header_line = " | ".join(tbl.headers)
            rows_text = []
            for row in tbl.rows:
                row_cells = [c.text.strip() for c in row]
                rows_text.append(" | ".join(row_cells))
            content = "header: " + header_line + "\n" + "\n".join(rows_text)
            chunk_id = f"{doc.doc_id}-table-{idx}"
            page_refs = [tbl.page]
            ldu = LDU(
                doc_id=doc.doc_id,
                chunk_id=chunk_id,
                content=content,
                chunk_type="table",
                page_refs=page_refs,
                bounding_box=tbl.bbox,
                parent_section="",
                token_count=len(content.split()),
                content_hash=self._hash(content),
            )
            table_ldus.append(ldu)
        return table_ldus

    def _chunk_text_blocks(self, doc: ExtractedDocument) -> List[LDU]:
        ldus: List[LDU] = []
        for i, tb in enumerate(doc.text_blocks):
            content = tb.text.strip()
            if not content:
                continue
            chunk_id = f"{doc.doc_id}-p{tb.page}-b{i}"
            ldu = LDU(
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
            ldus.append(ldu)
        return ldus

    def chunk(self, doc: ExtractedDocument) -> List[LDU]:
        ldus: List[LDU] = []
        ldus.extend(self._chunk_text_blocks(doc))
        ldus.extend(self._chunk_tables(doc))
        # TODO: add figures and numbered lists as separate chunk types
        self.validator.validate(ldus)
        return ldus
