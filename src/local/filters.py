import weaviate
import weaviate.classes.query as wq
import json

client = weaviate.connect_to_local()

questions = client.collections.get("Question")

# Filter "ANIMALS" categories
response = questions.query.hybrid(
    query="animal", limit=5,
    return_metadata=wq.MetadataQuery(score=True),
    filters=wq.Filter.by_property("category").equal("ANIMALS")
)

for obj in response.objects:
    print(json.dumps(obj.properties, indent=2))

client.close()  # Free up resources
