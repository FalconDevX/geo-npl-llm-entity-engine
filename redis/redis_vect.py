import polars as pl
from database import engine
from sentence_transformers import SentenceTransformer
import redis

r = redis.Redis( host='127.0.0.1', port=6379, db=0, decode_responses=True, encoding="utf-8" )
model = SentenceTransformer('sdadas/mmlw-retrieval-roberta-large')

query = "SELECT kod, nazwa, typ, text_for_vector FROM teryt_all"
pdf = pl.read_database(query=query, connection=engine)

pipeline_size = 10000 
model_batch_size = 64
start_index = 0 

df_to_process = pdf.slice(start_index)

for i in range(0, len(df_to_process), pipeline_size):
    pipeline_df = df_to_process.slice(i, pipeline_size)
    pipe = r.pipeline(transaction=False)
    
    texts = pipeline_df["text_for_vector"].to_list()
    embeddings = model.encode(
        texts, 
        batch_size=model_batch_size, 
        show_progress_bar=True, 
        convert_to_numpy=True
    )

    for j, row in enumerate(pipeline_df.iter_rows(named=True)):
        redis_key = f"geo:{row['kod']}"
        pipe.hset(redis_key, mapping={
            "v": embeddings[j].astype('float32').tobytes(),
            "nazwa": str(row['nazwa']),
            "kod": str(row['kod']),
            "typ": str(row['typ'])
        })
    
    pipe.execute()
    print(f"Progress: {start_index + i + len(pipeline_df)} / {len(pdf)}")