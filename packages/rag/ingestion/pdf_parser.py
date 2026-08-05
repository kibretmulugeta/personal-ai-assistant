"""
PDF Document Parser implementation.
Extracts text page by page from PDF binaries.
"""

import hashlib
import io
from packages.rag.ingestion.base import BaseDocumentParser, ParsedDocument

try:
    import pypdf
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False


class PDFDocumentParser(BaseDocumentParser):
    """Parser for PDF documents."""

    async def parse(self, file_content: bytes, filename: str) -> ParsedDocument:
        checksum = hashlib.sha256(file_content).hexdigest()
        extracted_text = ""
        metadata = {"page_count": 0}

        if HAS_PYPDF:
            try:
                reader = pypdf.PdfReader(io.BytesIO(file_content))
                metadata["page_count"] = len(reader.pages)
                pages_text = []
                for idx, page in enumerate(reader.pages):
                    txt = page.extract_text() or ""
                    if txt.strip():
                        pages_text.append(f"--- Page {idx + 1} ---\n{txt}")
                extracted_text = "\n\n".join(pages_text)
            except Exception as e:
                extracted_text = f"[PDF Parsing Warning: {str(e)}]\n" + file_content.decode("latin1", errors="ignore")
        else:
            # Fallback text extraction for environments without pypdf
            extracted_text = file_content.decode("latin1", errors="ignore")

        return ParsedDocument(
            filename=filename,
            file_type="pdf",
            content=extracted_text,
            checksum=checksum,
            metadata=metadata,
        )
