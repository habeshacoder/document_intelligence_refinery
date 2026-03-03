from pathlib import Path

from src.models.extracted_document import ExtractedDocument
from src.strategies.base import BaseExtractor, ExtractionResult


class LayoutExtractor(BaseExtractor):
    def extract(self, pdf_path: Path) -> ExtractionResult:
        # TODO: integrate MinerU or Docling and adapt their output to ExtractedDocument
        raise NotImplementedError(
            "LayoutExtractor must be implemented with MinerU or Docling."
        )
