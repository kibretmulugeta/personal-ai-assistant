"""
Abstract base document parser interface and ParsedDocument data model.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class ParsedDocument(BaseModel):
    """Normalized output from document parsing."""

    filename: str = Field(..., description="Original filename")
    file_type: str = Field(..., description="Detected extension (pdf, docx, txt, md)")
    content: str = Field(..., description="Extracted plain text content")
    checksum: str = Field(..., description="SHA256 content checksum")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Extracted metadata attributes")


class BaseDocumentParser(ABC):
    """Abstract interface for file type parsers."""

    @abstractmethod
    async def parse(self, file_content: bytes, filename: str) -> ParsedDocument:
        """Parse raw file bytes into ParsedDocument object.

        Args:
            file_content: Raw byte contents of the file.
            filename: File name string.

        Returns:
            ParsedDocument with extracted text and metadata.
        """
        pass
