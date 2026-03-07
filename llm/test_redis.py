import numpy as np
from sentence_transformers import SentenceTransformer
import redis
from dotenv import load_dotenv
import os

model = SentenceTransformer("BAAI/bge-m3", device="cuda")

load_dotenv()

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    db=os.getenv("REDIS_DB")
)

query = "powiat zamojski"

vector = model.encode(query).astype(np.float32)

q = "*=>[KNN 10 @embedding $vec AS score]"

res = redis_client.ft("teryt_vector_idx").search(
    q,
    query_params={"vec": vector.tobytes()}
)

for doc in res.docs:
    print(doc.text_for_vector)