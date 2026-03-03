from pathlib import Path

from src.models.extracted_document import ExtractedDocument
from src.strategies.base import BaseExtractor, ExtractionResult


class VisionExtractor(BaseExtractor):
    def __init__(self, budget_cap_usd: float = 0.5):
        self.budget_cap_usd = budget_cap_usd

    def extract(self, pdf_path: Path) -> ExtractionResult:
        # TODO: call VLM (e.g., via OpenRouter) on page images with budget guard
        raise NotImplementedError(
            "VisionExtractor must be implemented with a VLM backend."
        )
