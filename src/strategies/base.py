from pathlib import Path
from abc import ABC, abstractmethod
from typing import NamedTuple

from src.models.extracted_document import ExtractedDocument


class ExtractionResult(NamedTuple):
    doc: ExtractedDocument
    confidence: float
    cost_estimate: float


class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, pdf_path: Path) -> ExtractionResult: ...
