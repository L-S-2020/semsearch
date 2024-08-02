import chromadb, os

client = chromadb.HttpClient()
collection_search = client.get_or_create_collection(name="search")

# get data
metadata = []
content = []
ids = []
for filename in os.listdir("scrapes"):
    file = open("scrapes/" + filename, "r")
    url = file.readline().strip('\n')
    name = file.readline().strip('\n')
    text = file.readline().strip('\n')
    metadata.append({"url": url, "name": name})
    content.append(text)
    ids.append(filename.split(".txt")[0])

collection_search.add(
    documents=content,
    metadatas=metadata,
    ids=ids,
)

results = collection_search.query(
    query_texts=["How are my data stored?"],
    n_results=4
)

print(results)

