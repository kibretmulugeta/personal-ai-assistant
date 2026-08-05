"""
ContactSubmission model for visitor inquiries sent through the Digital Twin assistant.
"""

from typing import Optional
from sqlalchemy import String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from packages.database.models.base import BaseModel


class ContactSubmission(BaseModel):
    """Represents a contact request submitted by website visitors."""

    __tablename__ = "contact_submissions"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    subject: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        String(50), default="new", nullable=False
    )  # new | read | replied | archived
    metadata_json: Mapped[Optional[dict]] = mapped_column(JSON, default=dict, nullable=True)
