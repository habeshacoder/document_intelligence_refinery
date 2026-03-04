from pathlib import Path
from typing import List

from docling.document_converter import DocumentConverter

from src.models.extracted_document import (
    ExtractedDocument,
    TextBlock,
    Table,
    TableCell,
    Figure,
)
from src.strategies.base import BaseExtractor, ExtractionResult


class LayoutExtractor(BaseExtractor):
    def __init__(self):
        # Docling converter with PDF backend
        self.converter = DocumentConverter()

    def extract(self, pdf_path: Path) -> ExtractionResult:
        # Run Docling conversion
        result = self.converter.convert(str(pdf_path))
        doc = result.document  # DoclingDocument

        text_blocks: List[TextBlock] = []
        tables: List[Table] = []
        figures: List[Figure] = []

        # Text blocks
        for block in doc.text_blocks:
            # Docling blocks have page, bbox, text fields
            bbox = (
                float(block.bbox.x0),
                float(block.bbox.y0),
                float(block.bbox.x1),
                float(block.bbox.y1),
            )
            text_blocks.append(
                TextBlock(
                    page=block.page,
                    bbox=bbox,
                    text=block.text,
                )
            )

        # Tables
        for t in doc.tables:
            headers = [h.text for h in t.header_cells]
            rows: List[List[TableCell]] = []
            for r_idx, row in enumerate(t.body_rows):
                row_cells: List[TableCell] = []
                for c_idx, cell in enumerate(row.cells):
                    cb = cell.bbox
                    row_cells.append(
                        TableCell(
                            row=r_idx,
                            col=c_idx,
                            text=cell.text,
                            bbox=(
                                float(cb.x0),
                                float(cb.y0),
                                float(cb.x1),
                                float(cb.y1),
                            ),
                        )
                    )
                rows.append(row_cells)
            tb = Table(
                page=t.page,
                bbox=(
                    float(t.bbox.x0),
                    float(t.bbox.y0),
                    float(t.bbox.x1),
                    float(t.bbox.y1),
                ),
                headers=headers,
                rows=rows,
            )
            tables.append(tb)

        # Figures
        for fig in doc.figures:
            fb = fig.bbox
            figures.append(
                Figure(
                    page=fig.page,
                    bbox=(float(fb.x0), float(fb.y0), float(fb.x1), float(fb.y1)),
                    caption=fig.caption,
                )
            )

        extracted = ExtractedDocument(
            doc_id=pdf_path.stem,
            text_blocks=text_blocks,
            tables=tables,
            figures=figures,
        )

        confidence = 0.9  # Docling is strong for layout
        cost_estimate = 0.0  # local CPU cost

        return ExtractionResult(
            doc=extracted, confidence=confidence, cost_estimate=cost_estimate
        )
