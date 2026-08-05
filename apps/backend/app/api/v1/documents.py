"""
Document Upload and Ingestion Management API Router.
Handles file uploads (PDF, DOCX, TXT, MD), recursive chunking, embedding generation, and pgvector storage.
"""

from typing import List
from fastapi import APIRouter, Depends, File, UploadFile, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.api.deps import get_db_session
from packages.database.repositories.document_repo import DocumentRepository
from packages.rag.chunking.recursive_chunker import RecursiveCharacterChunker
from packages.rag.embeddings.factory import EmbeddingFactory
from packages.rag.ingestion.docx_parser import DOCXDocumentParser
from packages.rag.ingestion.pdf_parser import PDFDocumentParser
from packages.rag.ingestion.text_parser import TextDocumentParser
from packages.rag.retrieval.vector_store import VectorStore
from packages.shared.exceptions import ValidationException

router = APIRouter(prefix="/documents", tags=["Document Ingestion"])


class DocumentResponse(BaseModel):
    """Document metadata response."""

    id: str = Field(..., description="Document UUID")
    filename: str = Field(..., description="File name")
    file_type: str = Field(..., description="File extension")
    checksum: str = Field(..., description="SHA256 checksum")
    status: str = Field(..., description="Ingestion status")


@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db_session),
) -> DocumentResponse:
    """Upload and ingest a document (PDF, DOCX, TXT, MD) into pgvector database."""
    filename = file.filename or "uploaded_file.txt"
    ext = filename.split(".")[-1].lower() if "." in filename else "txt"

    file_content = await file.read()
    if not file_content:
        raise ValidationException(message="Uploaded file is empty.")

    # Select Parser
    if ext == "pdf":
        parser = PDFDocumentParser()
    elif ext in ["docx", "doc"]:
        parser = DOCXDocumentParser()
    elif ext in ["txt", "md", "markdown", "json", "csv"]:
        parser = TextDocumentParser()
    else:
        raise ValidationException(message=f"Unsupported file extension '.{ext}'. Supported: pdf, docx, txt, md, csv, json.")

    parsed_doc = await parser.parse(file_content=file_content, filename=filename)

    # Chunking
    chunker = RecursiveCharacterChunker(chunk_size=500, chunk_overlap=50)
    chunks = chunker.split_text(parsed_doc.content)

    # Embeddings & Vector Storage
    embedding_provider = EmbeddingFactory.get_provider()
    vector_store = VectorStore(session=db, embedding_provider=embedding_provider)
    doc_record = await vector_store.ingest_parsed_document(parsed_doc=parsed_doc, text_chunks=chunks)

    return DocumentResponse(
        id=str(doc_record.id),
        filename=doc_record.filename,
        file_type=doc_record.file_type,
        checksum=doc_record.checksum,
        status=doc_record.status,
    )


@router.get("", response_model=List[DocumentResponse], status_code=status.HTTP_200_OK)
async def list_documents(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db_session),
) -> List[DocumentResponse]:
    """List ingested knowledge base documents."""
    repo = DocumentRepository(session=db)
    docs = await repo.list_all(skip=skip, limit=limit)
    return [
        DocumentResponse(
            id=str(d.id),
            filename=d.filename,
            file_type=d.file_type,
            checksum=d.checksum,
            status=d.status,
        )
        for d in docs
    ]
