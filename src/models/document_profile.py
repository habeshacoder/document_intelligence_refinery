from pydantic import BaseModel
from typing import Literal


class DocumentProfile(BaseModel):
    doc_id: str
    origin_type: Literal["native_digital", "scanned_image", "mixed", "form_fillable"]
    layout_complexity: Literal["single_column", "multi_column", "table_heavy", "figure_heavy", "mixed"]
    language: str
    language_confidence: float
    domain_hint: Literal["financial", "legal", "technical", "medical", "general"]
    estimated_extraction_cost: Literal["fast_text_sufficient", "needs_layout_model", "needs_vision_model"]
