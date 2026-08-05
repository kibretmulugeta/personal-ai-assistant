# RAG Pipeline Documentation

**Retrieval-Augmented Generation Architecture**

---

## 1. Pipeline Lifecycle

```text
[Document Upload (PDF, DOCX, TXT, MD)]
                │
                ▼
[Document Parsers (pdf_parser.py, docx_parser.py, text_parser.py)]
                │
                ▼
[SHA256 Checksum Duplicate Check & Metadata Extraction]
                │
                ▼
[Recursive Character Chunker (500 chars, 50 char overlap)]
                │
                ▼
[Embedding Generation (OpenAI text-embedding-3-small / BGE)]
                │
                ▼
[pgvector Storage (document_chunks table with Vector(1536))]
                │
                ▼
[Similarity Search (<=> Cosine Distance) & Citation Assembly]
```

---

## 2. Source Attributions & Citations

Every retrieved chunk includes citation metadata returned to the frontend:
- `document_id`: Document UUID
- `filename`: Source document name
- `chunk_index`: Zero-based chunk index
- `similarity_score`: Vector distance
- `snippet`: Content excerpt
