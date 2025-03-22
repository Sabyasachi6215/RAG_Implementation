
"SmartRAG: Boosted Document QA using Hybrid Multi-query Retrieval &amp; Re-ranking"

# RAG_Implementation

User Query
   ↓
Multi-query generation (e.g., 3 query variants)
   ↓
Hybrid Retrieval (BM25 + Dense Vector Search for each query)
   ↓
Reciprocal Rank Fusion (combine results from all queries & retrievers)
   ↓
Top-K Documents
   ↓
Pass to LLM (with prompt template)
   ↓
Generated Answer


# Case : 1

## Multi-query Retrieval

![alt text](image.png)
![alt text](image-1.png)
Instead of using just one query, you generate multiple variations of the user query (via paraphrasing, different phrasings, or prompt rewordings).

This helps capture different intents or nuances that a single query might miss.

These queries are issued in parallel, and results are merged.

Benefit: Improves recall (fetches more relevant results).

Example:

User asks: "How do I fix a flat tire?"
You might also query:

"Steps to repair a bicycle tire",

"Flat tire troubleshooting",

"How to patch a tire tube?"
...then merge the best answers.

# Case : 2

## Hybrid Retrieval

🧪 Hybrid Retrieval
Combines sparse and dense retrieval:

Sparse: Traditional keyword-based search (e.g., BM25)

Dense: Semantic search using vector embeddings (bi-encoders)

Why hybrid? Each method captures different strengths—keywords work well for exact matches, dense works better for semantic similarity.

Example:

"apple" could mean the fruit or the company. Sparse might match documents with the literal word "apple", while dense embeddings capture meaning based on context.