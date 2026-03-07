from redis.commands.search.query import Query
import numpy as np
from sentence_transformers import SentenceTransformer
import redis
import os
from dotenv import load_dotenv
import difflib
import unidecode

load_dotenv()

model = SentenceTransformer("BAAI/bge-m3", device="cuda")

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    db=int(os.getenv("REDIS_DB")),
    password=os.getenv("REDIS_PASSWORD")
)

query_text = "warszawa"

normalized = unidecode.unidecode(query_text.lower())

words = normalized.split()
text_query = " ".join([f"%{w}%|{w}*" for w in words])

q = Query(
    f"@text_for_vector:{text_query}"
).return_fields(
    "teryt",
    "text_for_vector",
    "embedding"
).paging(0, 50)

res = redis_client.ft("teryt_vector_idx").search(q)

docs = res.docs

query_vec = model.encode(
    f"miejscowosc {normalized} w polsce",
    normalize_embeddings=True
).astype(np.float32)


def cosine(a, b):
    return np.dot(a, b)


def _place_name(text: str) -> str:
    text = unidecode.unidecode(text.lower())
    return text.split(",")[0].strip()


def fuzzy_score(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a, _place_name(b)).ratio()


def prefix_match(a: str, b: str) -> float:
    return 1.0 if _place_name(b).startswith(a) else 0.0

ranked = []

for doc in docs:

    emb = np.frombuffer(doc.embedding, dtype=np.float32)

    vec_score = cosine(query_vec, emb)
    f_score = fuzzy_score(normalized, doc.text_for_vector)
    p_score = prefix_match(normalized, doc.text_for_vector)

    final_score = vec_score * 0.5 + f_score * 0.3 + p_score * 0.2

    ranked.append((final_score, doc))

ranked.sort(key=lambda x: x[0], reverse=True)

print("\nRESULTS:\n")

for score, doc in ranked[:10]:
    print(doc.teryt, doc.text_for_vector, score)

best = ranked[0][1]

print("\n\033[92mBEST MATCH:\033[0m", best.teryt, best.text_for_vector)