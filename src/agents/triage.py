from pathlib import Path
from typing import Optional

import pdfplumber
from pydantic import BaseModel

from src.models.document_profile import DocumentProfile


class PageStats(BaseModel):
    page: int
    char_count: int
    char_density: float
    image_area_ratio: float


class TriageAgent:
    def __init__(self, rules_path: Optional[Path] = None):
        self.rules_path = rules_path

    def _compute_page_stats(self, pdf_path: Path) -> list[PageStats]:
        stats: list[PageStats] = []
        with pdfplumber.open(str(pdf_path)) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                width, height = page.width, page.height
                area = width * height
                text = page.extract_text() or ""
                char_count = len(text)
                images = page.images or []
                img_area = sum(img["width"] * img["height"] for img in images)
                image_area_ratio = img_area / area if area else 0.0
                char_density = char_count / area if area else 0.0
                stats.append(
                    PageStats(
                        page=i,
                        char_count=char_count,
                        char_density=char_density,
                        image_area_ratio=image_area_ratio,
                    )
                )
        return stats

    def profile_document(self, pdf_path: Path) -> DocumentProfile:
        stats = self._compute_page_stats(pdf_path)
        avg_density = sum(s.char_density for s in stats) / max(len(stats), 1)
        avg_img_ratio = sum(s.image_area_ratio for s in stats) / max(len(stats), 1)

        if avg_density < 0.0005 and avg_img_ratio > 0.5:
            origin_type = "scanned_image"
            estimated_cost = "needs_vision_model"
        else:
            origin_type = "native_digital"
            estimated_cost = "fast_text_sufficient"

        # Simple heuristic for layout complexity (can be refined)
        if any(s.char_count > 2000 for s in stats):
            layout_complexity = "multi_column"
        else:
            layout_complexity = "single_column"

        # TODO: plug in language detection (e.g., fastText, langdetect)
        language = "en"
        language_confidence = 0.9

        # TODO: keyword-based domain detection
        domain_hint = "general"

        return DocumentProfile(
            doc_id=pdf_path.stem,
            origin_type=origin_type,
            layout_complexity=layout_complexity,
            language=language,
            language_confidence=language_confidence,
            domain_hint=domain_hint,
            estimated_extraction_cost=estimated_cost,
        )
