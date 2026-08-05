"""
Document Ingestion subpackage initialization.
"""

from packages.rag.ingestion.base import BaseDocumentParser, ParsedDocument
from packages.rag.ingestion.docx_parser import DOCXDocumentParser
from packages.rag.ingestion.pdf_parser import PDFDocumentParser
from packages.rag.ingestion.text_parser import TextDocumentParser

__all__ = [
    "BaseDocumentParser",
    "ParsedDocument",
    "PDFDocumentParser",
    "DOCXDocumentParser",
    "TextDocumentParser",
]
