# retriever.py
# RAG leve: embeddings por hashing + cosine similarity + bônus por palavra-chave

import math
import re

def load_conhecimento():
    with open("conhecimento/conhecimento.txt", "r", encoding="utf-8") as f:
        return f.read()

def _chunk_text(text: str, chunk_size: int = 900, overlap: int = 150):
    text = text.strip()
    if not text:
        return []

    chunks = []
    i = 0
    while i < len(text):
        end = min(len(text), i + chunk_size)
        chunk = text[i:end].strip()
        if chunk:
            chunks.append(chunk)
        i += max(1, chunk_size - overlap)
    return chunks

def _tokenize(s: str):
    return re.findall(r"[a-zA-ZÀ-ÿ0-9]+", (s or "").lower())

def _hash_embedding(text: str, dim: int = 384):
    vec = [0.0] * dim
    tokens = _tokenize(text)

    for tok in tokens:
        h = hash(tok) % dim
        vec[h] += 1.0

    norm = math.sqrt(sum(v*v for v in vec)) or 1.0
    return [v / norm for v in vec]

def _cosine(a, b):
    return sum(x*y for x, y in zip(a, b))

_cached_chunks = []
_cached_vectors = []
_cached_ready = False

def build_index(conhecimento_text: str):
    global _cached_chunks, _cached_vectors, _cached_ready
    _cached_chunks = _chunk_text(conhecimento_text)
    _cached_vectors = [_hash_embedding(ch) for ch in _cached_chunks]
    _cached_ready = True

def simple_retriever(query, conhecimento, top_k: int = 4):
    global _cached_ready

    if not _cached_ready:
        build_index(conhecimento)

    if not _cached_chunks:
        return ""

    qv = _hash_embedding(query)
    importantes = [t for t in _tokenize(query) if len(t) >= 5]

    scored = []
    for ch, cv in zip(_cached_chunks, _cached_vectors):
        base = _cosine(qv, cv)

        # bônus por palavra-chave (melhora muito precisão)
        ch_low = ch.lower()
        bonus = 0.0
        for t in importantes:
            if t in ch_low:
                bonus += 0.20

        scored.append((base + bonus, ch))

    scored.sort(key=lambda x: x[0], reverse=True)

    top = [ch for score, ch in scored[:top_k] if score > 0]

    # se não achou nada relevante, devolve vazio (o LLM decide "não encontrado")
    return "\n\n---\n\n".join(top)