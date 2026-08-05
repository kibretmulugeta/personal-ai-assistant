"""
Recursive character text chunker.
Splits text recursively using double newlines, newlines, spaces, and punctuation to maintain semantic structure.
"""

from typing import Any, Dict, List
from pydantic import BaseModel, Field


class TextChunk(BaseModel):
    """Chunk model containing content text, index, character range, and metadata."""

    chunk_index: int = Field(..., description="Zero-based index of chunk")
    content: str = Field(..., description="Text content of the chunk")
    start_char: int = Field(..., description="Start character offset")
    end_char: int = Field(..., description="End character offset")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata attributes")


class RecursiveCharacterChunker:
    """Splits long text into overlapping chunks using hierarchical delimiters."""

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        separators: List[str] = None,
    ) -> None:
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", ". ", " ", ""]

    def split_text(self, text: str) -> List[TextChunk]:
        """Split text into a list of TextChunk items."""
        if not text or not text.strip():
            return []

        chunks: List[TextChunk] = []
        start_idx = 0
        text_length = len(text)
        chunk_counter = 0

        while start_idx < text_length:
            end_idx = min(start_idx + self.chunk_size, text_length)

            if end_idx < text_length:
                # Search for best separator near end_idx
                best_cut = end_idx
                for sep in self.separators:
                    if not sep:
                        continue
                    last_sep = text.rfind(sep, start_idx + self.chunk_overlap, end_idx)
                    if last_sep != -1:
                        best_cut = last_sep + len(sep)
                        break
                end_idx = best_cut

            chunk_str = text[start_idx:end_idx].strip()
            if chunk_str:
                chunks.append(
                    TextChunk(
                        chunk_index=chunk_counter,
                        content=chunk_str,
                        start_char=start_idx,
                        end_char=end_idx,
                        metadata={"length": len(chunk_str)},
                    )
                )
                chunk_counter += 1

            if end_idx >= text_length:
                break

            # Advance with overlap
            start_idx = max(start_idx + 1, end_idx - self.chunk_overlap)

        return chunks
