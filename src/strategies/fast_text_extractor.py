from pathlib import Path

import pdfplumber

from src.models.extracted_document import ExtractedDocument, TextBlock, Table, Figure
from src.strategies.base import BaseExtractor, ExtractionResult


class FastTextExtractor(BaseExtractor):
    def extract(self, pdf_path: Path) -> ExtractionResult:
        text_blocks: list[TextBlock] = []
        tables: list[Table] = []
        figures: list[Figure] = []

        with pdfplumber.open(str(pdf_path)) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                words = page.extract_words() or []
                if words:
                    x0 = min(w["x0"] for w in words)
                    top = min(w["top"] for w in words)
                    x1 = max(w["x1"] for w in words)
                    bottom = max(w["bottom"] for w in words)
                    text = page.extract_text() or ""
                    text_blocks.append(
                        TextBlock(page=i, bbox=(x0, top, x1, bottom), text=text)
                    )

        doc = ExtractedDocument(
            doc_id=pdf_path.stem,
            text_blocks=text_blocks,
            tables=tables,
            figures=figures,
        )

        total_chars = sum(len(tb.text) for tb in text_blocks)
        confidence = 1.0 if total_chars > 500 else 0.3
        cost_estimate = 0.0

        return ExtractionResult(
            doc=doc, confidence=confidence, cost_estimate=cost_estimate
        )
