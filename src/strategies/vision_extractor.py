from pathlib import Path
from typing import List

import pdfplumber
import pytesseract
from PIL import Image

from src.models.extracted_document import ExtractedDocument, TextBlock, Table, Figure
from src.strategies.base import BaseExtractor, ExtractionResult


class VisionExtractor(BaseExtractor):
    def __init__(self, budget_cap_usd: float = 0.5):
        self.budget_cap_usd = budget_cap_usd

    def extract(self, pdf_path: Path) -> ExtractionResult:
        text_blocks: List[TextBlock] = []
        tables: List[Table] = []
        figures: List[Figure] = []

        with pdfplumber.open(str(pdf_path)) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                # render page to image
                pil_image: Image.Image = page.to_image(resolution=300).original
                text = pytesseract.image_to_string(pil_image) or ""
                if text.strip():
                    bbox = (0.0, 0.0, float(page.width), float(page.height))
                    text_blocks.append(TextBlock(page=i, bbox=bbox, text=text))

        extracted = ExtractedDocument(
            doc_id=pdf_path.stem,
            text_blocks=text_blocks,
            tables=tables,
            figures=figures,
        )

        total_chars = sum(len(tb.text) for tb in text_blocks)
        confidence = 1.0 if total_chars > 300 else 0.4
        # Rough cost estimate: CPU OCR only, no per-token cost
        cost_estimate = 0.0

        return ExtractionResult(
            doc=extracted, confidence=confidence, cost_estimate=cost_estimate
        )
