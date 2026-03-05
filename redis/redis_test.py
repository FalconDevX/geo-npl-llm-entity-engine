import numpy as np
from sentence_transformers import SentenceTransformer
import redis
from redis.commands.search.query import Query

model = SentenceTransformer('sdadas/mmlw-retrieval-roberta-large')

r = redis.Redis(host='127.0.0.1', port=6379, db=0)

def find_geo_match(user_input, top_k=3):
    query_vector = model.encode(user_input).astype('float32').tobytes()

    q = (
        Query(f"*=>[KNN {top_k} @v $vec AS score]")
        .return_fields("nazwa", "kod", "typ", "score")
        .sort_by("score")
        .dialect(2)
    )

    res = r.ft("idx:geo_spatial").search(q, query_params={"vec": query_vector})

    return [
        {
            "nazwa": doc.nazwa,
            "kod": doc.kod,
            "typ": doc.typ,
            "similarity": 1 - float(doc.score)  
        }
        for doc in res.docs
    ]

data = find_geo_match("wojewodztwo lubelske")
print(data)