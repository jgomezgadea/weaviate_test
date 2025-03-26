import weaviate
import weaviate.classes.query as wq
import json

client = weaviate.connect_to_local()

questions = client.collections.get("Question")

response = questions.query.hybrid(
    query="animal", limit=5, return_metadata=wq.MetadataQuery(score=True)
)

for obj in response.objects:
    print(json.dumps(obj.properties, indent=2))

client.close()  # Free up resources
