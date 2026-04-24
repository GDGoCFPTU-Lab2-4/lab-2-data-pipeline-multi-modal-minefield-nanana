from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

# ==========================================
# ROLE 1: LEAD DATA ARCHITECT
# ==========================================
# Your task is to define the Unified Schema for all sources.
# This is v1. Note: A breaking change is coming at 11:00 AM!


class UnifiedDocument(BaseModel):
    document_id: str
    content: str
    source_type: Literal[
        'PDF',
        'Video',
        'HTML',
        'CSV',
        'Code',
    ]  # e.g., 'PDF', 'Video', 'HTML', 'CSV', 'Code'
    author: str | None = 'Unknown'
    timestamp: datetime | None = None

    # You might want a dict for source-specific metadata
    source_metadata: dict[str, object] = Field(default_factory=dict)
