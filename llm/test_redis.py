import numpy as np
from sentence_transformers import SentenceTransformer
import redis
from dotenv import load_dotenv
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

load_dotenv()

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    db=os.getenv("REDIS_DB")
)

query = "warszawa"

vector = model.encode(query).astype(np.float32)

q = "*=>[KNN 5 @vector $vec AS score]"

res = redis_client.ft("teryt_vector_idx").search(
    q,
    query_params={"vec": vector.tobytes()}
)

for doc in res.docs:
    print(doc.text)