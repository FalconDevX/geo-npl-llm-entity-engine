import redis

from redis.commands.search.field import VectorField, TextField, TagField
from redis.commands.search.index_definition import IndexDefinition, IndexType

r = redis.Redis(host='127.0.0.1', port=6379, db=0)

INDEX_NAME = "idx:geo_spatial"

try:
    schema = (
        VectorField("v", "HNSW", {
            "TYPE": "FLOAT32",
            "DIM": 1024,              
            "DISTANCE_METRIC": "COSINE" 
        }),
        TextField("nazwa"),
        TagField("typ"),
        TextField("kod")
    )

    definition = IndexDefinition(prefix=["geo:"], index_type=IndexType.HASH)

    r.ft(INDEX_NAME).create_index(fields=schema, definition=definition)
    print("Index created successfully!")
except Exception as e:
    print(f"Error (maybe index already exists?): {e}")