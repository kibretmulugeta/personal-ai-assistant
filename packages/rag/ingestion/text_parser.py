"""
Text, Markdown, HTML, JSON, and CSV Parser implementation.
"""

import hashlib
from packages.rag.ingestion.base import BaseDocumentParser, ParsedDocument


class TextDocumentParser(BaseDocumentParser):
    """Parser for plain text, Markdown, CSV, JSON, and HTML documents."""

    async def parse(self, file_content: bytes, filename: str) -> ParsedDocument:
        checksum = hashlib.sha256(file_content).hexdigest()
        
        # Determine extension
        ext = filename.split(".")[-1].lower() if "." in filename else "txt"
        
        try:
            content_str = file_content.decode("utf-8")
        except UnicodeDecodeError:
            content_str = file_content.decode("latin1", errors="ignore")

        return ParsedDocument(
            filename=filename,
            file_type=ext,
            content=content_str,
            checksum=checksum,
            metadata={"character_count": len(content_str)},
        )
