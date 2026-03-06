import redis
import psycopg2
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os
from tqdm import tqdm

load_dotenv()

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    db=int(os.getenv("REDIS_DB"))
)

pg = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    database=os.getenv("POSTGRES_DATABASE"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)

cursor = pg.cursor()

model = SentenceTransformer("all-MiniLM-L6-v2")

cursor.execute("""
SELECT kod, text_for_vector
FROM teryt_all
WHERE text_for_vector IS NOT NULL
""")

rows = cursor.fetchall()

print("records:", len(rows))

BATCH_SIZE = 256

pipeline = redis_client.pipeline()

for i in tqdm(range(0, len(rows), BATCH_SIZE)):

    batch = rows[i:i+BATCH_SIZE]

    texts = [x[1] for x in batch]
    vectors = model.encode(texts, batch_size=64).astype(np.float32)

    for (kod, text), vector in zip(batch, vectors):

        pipeline.hset(
            f"teryt:{kod}",
            mapping={
                "kod": kod,
                "text": text,
                "vector": vector.tobytes()
            }
        )

    pipeline.execute()

print("vector database built")