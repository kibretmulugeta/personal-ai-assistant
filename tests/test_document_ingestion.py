"""
Unit tests for document parsers (PDF, DOCX, TXT) and recursive chunking.
"""

import pytest
from packages.rag.chunking.recursive_chunker import RecursiveCharacterChunker
from packages.rag.ingestion.pdf_parser import PDFDocumentParser
from packages.rag.ingestion.text_parser import TextDocumentParser


@pytest.mark.asyncio
async def test_text_parser():
    """Verify parsing plain text / markdown files."""
    parser = TextDocumentParser()
    raw_bytes = b"# Alemu Kibret Mulugeta\n\nAI Researcher specializing in Medical Image Segmentation."
    parsed = await parser.parse(raw_bytes, "sample.md")

    assert parsed.filename == "sample.md"
    assert parsed.file_type == "md"
    assert "Alemu Kibret" in parsed.content
    assert len(parsed.checksum) == 64


@pytest.mark.asyncio
async def test_pdf_parser_fallback():
    """Verify PDF parser handles input cleanly."""
    parser = PDFDocumentParser()
    raw_bytes = b"%PDF-1.4 sample content"
    parsed = await parser.parse(raw_bytes, "research_paper.pdf")

    assert parsed.file_type == "pdf"
    assert len(parsed.checksum) == 64


def test_recursive_character_chunker():
    """Verify text chunking splits long text with character overlap."""
    text = (
        "Alemu Kibret Mulugeta is an AI Researcher and Machine Learning Engineer. "
        "He holds an M.Sc. in Computer Engineering with specialization in Artificial Intelligence "
        "and Data Engineering from Bahir Dar University (2025). "
        "His research focuses on stroke lesion segmentation using hybrid U-Net architectures and metaheuristic optimization."
    )
    chunker = RecursiveCharacterChunker(chunk_size=100, chunk_overlap=20)
    chunks = chunker.split_text(text)

    assert len(chunks) > 1
    assert chunks[0].chunk_index == 0
    assert "Alemu" in chunks[0].content
