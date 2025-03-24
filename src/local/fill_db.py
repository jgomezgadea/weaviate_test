import requests, json
import weaviate
from weaviate.classes.config import Configure

# Connect to Weaviate
client = weaviate.connect_to_local()

if not client.is_ready():
    raise Exception("Weaviate is not ready")


# Create a new collection with Ollama integration
questions = client.collections.create(
    name="Question",
    vectorizer_config=Configure.Vectorizer.text2vec_ollama(     # Configure the Ollama embedding integration
        api_endpoint="http://host.docker.internal:11434",       # Allow Weaviate from within a Docker container to contact your Ollama instance
        model="nomic-embed-text",                               # The model to use
    ),
    generative_config=Configure.Generative.ollama(              # Configure the Ollama generative integration
        api_endpoint="http://host.docker.internal:11434",       # Allow Weaviate from within a Docker container to contact your Ollama instance
        model="llama3.2",                                       # The model to use
    )
)

# Load the data
resp = requests.get(
    "https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json"
)
data = json.loads(resp.text)
# questions = client.collections.get("Question")

with questions.batch.dynamic() as batch:
    for d in data:
        batch.add_object({
            "answer": d["Answer"],
            "question": d["Question"],
            "category": d["Category"],
        })
        if batch.number_errors > 10:
            print("Batch import stopped due to excessive errors.")
            break

failed_objects = questions.batch.failed_objects
if failed_objects:
    print(f"Number of failed imports: {len(failed_objects)}")
    print(f"First failed object: {failed_objects[0]}")

client.close() # Free up resources
