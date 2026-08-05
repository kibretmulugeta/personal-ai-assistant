"""
Document and DocumentChunk models for pgvector RAG pipeline storage.
Includes fallback handling if pgvector is not installed in local test environment.
"""

from typing import List, Optional
from sqlalchemy import String, Text, Integer, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from packages.database.models.base import BaseModel

try:
    from pgvector.sqlalchemy import Vector
    HAS_PGVECTOR = True
except ImportError:
    HAS_PGVECTOR = False
    Vector = lambda dim: JSON  # Fallback column type for non-postgres environments


class Document(BaseModel):
    """Represents an ingested knowledge base document (PDF, DOCX, TXT, MD, etc.)."""

    __tablename__ = "documents"

    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_type: Mapped[str] = mapped_column(String(50), nullable=False)
    storage_path: Mapped[str] = mapped_column(String(512), nullable=False)
    checksum: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    status: Mapped[str] = mapped_column(
        String(50), default="pending", nullable=False
    )
    metadata_json: Mapped[Optional[dict]] = mapped_column(JSON, default=dict, nullable=True)

    chunks: Mapped[List["DocumentChunk"]] = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete-orphan",
        order_by="DocumentChunk.chunk_index",
    )


class DocumentChunk(BaseModel):
    """Represents a text chunk and its corresponding vector embedding for semantic search."""

    __tablename__ = "document_chunks"

    document_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding = mapped_column(Vector(1536), nullable=True)
    metadata_json: Mapped[Optional[dict]] = mapped_column(JSON, default=dict, nullable=True)

    document: Mapped["Document"] = relationship("Document", back_populates="chunks")
