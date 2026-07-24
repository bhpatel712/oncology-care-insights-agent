"""
Search tool — Azure AI Search retrieval over NCI PDQ guideline chunks.
Registered as a tool on the Foundry Agent Service.
"""

# TODO Week 3: Implement search tool

def search_guidelines(query: str, cancer_type: str = None, stage: str = None) -> list:
    """
    Retrieves relevant NCI PDQ guideline chunks for a given query.
    Optionally filters by cancer_type and/or stage metadata.
    Returns list of chunks with text + source citation.
    """
    pass
