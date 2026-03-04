import polars as pl
from database import engine
from sentence_transformers import SentenceTransformer
import redis

r = redis.Redis(host='127.0.0.1', port=6379, db=0)

model = SentenceTransformer('sdadas/mmlw-retrieval-roberta-large')


print("Get data from postgres table database")

query = "SELECT kod, nazwa, typ, text_for_vector FROM teryt_all"

pdf = pl.read_database(query=query, connection = engine)

#generate embeddings for records
#redis pipline
pipe = r.pipeline()

for i, row in enumerate(pdf.iter_rows(named=True)):
    embedding = model.encode(row['text_for_vector']).astype('float32').tobytes()

    redis_key = f"geo:{row['kod']}"

    #save data as hask
    pipe.hset(redis_key, mapping={
        "v": embedding,
        "nazwa": row['nazwa'],
        "kod": row['kod'],
        "typ": row['typ']
    })

    if (i + 1) % 500 == 0:
        pipe.execute()
        print(f"Processed {i + 1} of {len(pdf)} records...")

pipe.execute()
print(f"Saved {len(pdf)} records to Redis")
