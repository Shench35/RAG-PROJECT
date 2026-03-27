from fastapi import APIRouter
import chromadb
import ollama

from src.app.get_keyword import keyword_getter
from src.app.emb_scraper import clean_text, scrape_wikipedia
from src.app.text_to_embed import to_embeding

main_route = APIRouter()
chroma = chromadb.PersistentClient(path="./db")
collection = chroma.get_or_create_collection("docs")
# client = ollama.Client(host="http://host.docker.internal:11434")
client = ollama.Client(host="http://127.0.0.1:11434")

@main_route.post("/query")
def query(q: str):
    get_keyword = keyword_getter(q)
    print(get_keyword)
    existing = collection.get(ids=[get_keyword])
    print(existing)
    if not existing["documents"]:
        result = scrape_wikipedia(get_keyword)
        clean_text_result = clean_text(result["text"])
        to_embeding(clean_text_result, get_keyword)
        
    results = collection.query(query_texts=[q], n_results=1)
    print(results)
    context = results["documents"][0][0] if results["documents"] else ""
    print(f"Context retrieved: {context}")

    answer = client.generate(
        model="tinyllama",
        prompt=f"Context:\n{context}\n\nQuestion: {q}\n\nAnswer clearly and concisely:"
    )

    return {"answer": answer["response"]}
