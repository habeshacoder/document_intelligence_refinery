from pathlib import Path
import json
import time
from dataclasses import dataclass
from typing import Optional

from src.models.document_profile import DocumentProfile
from src.models.extracted_document import ExtractedDocument
from src.strategies.fast_text_extractor import FastTextExtractor
from src.strategies.layout_extractor import LayoutExtractor
from src.strategies.vision_extractor import VisionExtractor
from src.strategies.base import ExtractionResult


@dataclass
class ExtractionLedgerEntry:
    doc_id: str
    strategy_used: str
    confidence_score: float
    cost_estimate: float
    processing_time_sec: float


class ExtractionRouter:
    def __init__(self, ledger_path: Optional[Path] = None):
        self.fast = FastTextExtractor()
        self.layout = LayoutExtractor()
        self.vision = VisionExtractor()
        self.ledger_path = ledger_path or Path(".refinery/extraction_ledger.jsonl")

    def _log(self, entry: ExtractionLedgerEntry) -> None:
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        with self.ledger_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry.__dict__) + "\n")

    def extract(self, pdf_path: Path, profile: DocumentProfile) -> ExtractedDocument:
        start = time.time()

        if (
            profile.origin_type == "native_digital"
            and profile.layout_complexity == "single_column"
        ):
            strategy = "fast"
            result: ExtractionResult = self.fast.extract(pdf_path)
            if result.confidence < 0.7:
                strategy = "layout"
                result = self.layout.extract(pdf_path)
        elif profile.origin_type == "scanned_image":
            strategy = "vision"
            result = self.vision.extract(pdf_path)
        else:
            strategy = "layout"
            result = self.layout.extract(pdf_path)

        elapsed = time.time() - start
        self._log(
            ExtractionLedgerEntry(
                doc_id=profile.doc_id,
                strategy_used=strategy,
                confidence_score=result.confidence,
                cost_estimate=result.cost_estimate,
                processing_time_sec=elapsed,
            )
        )
        return result.doc
