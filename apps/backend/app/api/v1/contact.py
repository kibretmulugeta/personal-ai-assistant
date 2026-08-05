"""
Contact Form Submission API Router.
"""

from typing import Optional
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.api.deps import get_db_session
from packages.database.repositories.contact_repo import ContactSubmissionRepository

router = APIRouter(prefix="/contact", tags=["Contact"])


class ContactFormRequest(BaseModel):
    """Contact form submission payload."""

    name: str = Field(..., min_length=2, max_length=255, description="Sender full name")
    email: EmailStr = Field(..., description="Sender contact email address")
    subject: Optional[str] = Field(default="Inquiry via Portfolio AI Assistant", max_length=255)
    message: str = Field(..., min_length=5, description="Message text body")


class ContactFormResponse(BaseModel):
    """Contact submission confirmation."""

    success: bool = True
    message: str = "Thank you for getting in touch! Your message has been received."
    submission_id: str


@router.post("/submit", response_model=ContactFormResponse, status_code=status.HTTP_201_CREATED)
async def submit_contact_form(
    request: ContactFormRequest,
    db: AsyncSession = Depends(get_db_session),
) -> ContactFormResponse:
    """Submit a contact message to Alemu Kibret Mulugeta."""
    repo = ContactSubmissionRepository(session=db)
    submission = await repo.create(
        name=request.name,
        email=request.email,
        subject=request.subject,
        message=request.message,
        status="new",
    )
    return ContactFormResponse(
        success=True,
        message="Thank you for getting in touch! Your message has been received.",
        submission_id=str(submission.id),
    )
