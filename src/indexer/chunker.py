"""
Chunker — splits NCI PDQ guideline text into embeddable chunks.
Target chunk size: 500–800 tokens with overlap.
Each chunk is tagged with: cancer_type, stage, section, source_url
"""

# TODO Week 2: Implement chunking logic

def chunk_document(text: str, cancer_type: str, source_url: str, chunk_size: int = 700, overlap: int = 100) -> list:
    """
    Splits a guideline document into overlapping chunks with metadata.
    Returns list of dicts: {text, cancer_type, stage, section, source_url, chunk_id}
    """
    pass
