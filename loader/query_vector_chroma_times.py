import os
import time
import chromadb
import dotenv
from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.ollama import OllamaEmbedding

from embed_model import embed_model_name, collection_name
from prompt import prompt

dotenv.load_dotenv()

# 1. Configuración
embed_model = OllamaEmbedding(model_name=embed_model_name)

# llm_model = Ollama(model="mistral:latest")
llm_model = OpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))

remote_db = chromadb.HttpClient(host='localhost', port=8000)
chroma_collection = remote_db.get_collection(collection_name)
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store, embed_model=embed_model)

# query_str = "Explicame sobre los nivel de seguridad en la firma electrónica"
# query_str = "Cuales son los errores de los comprobantes rechazados que pueden volver solicitar?"
query_str = "Cuales son los valores sub totales y totales con impuestos que deben constar en los comprobantes de venta?"

# --- PASO 1: MEDICIÓN DEL EMBEDDING ---
# print("Generando embedding de la consulta...")
# start_emb = time.time()
# query_embedding = embed_model.get_query_embedding(query_str)
# end_emb = time.time()
# print(f"Tiempo solo para generar el vector: {end_emb - start_emb:.4f} seg")

# --- PASO 2: RETRIEVAL (BÚSQUEDA EN CHROMADB) ---
print("Realizando búsqueda en ChromaDB...")
retriever = index.as_retriever(similarity_top_k=3)
start_ret = time.time()
nodes = retriever.retrieve(query_str)
end_ret = time.time()
print(
    f"Tiempo de búsqueda en DB (con embedding incluido si se llama vía retriever): {end_ret - start_ret:.4f} seg")
# Si esto es 0, por eso la generación es rápida
print(f"Nodos recuperados: {len(nodes)}")

# --- PASO 3: GENERACIÓN (LLM) ---
print("Generando respuesta con LLM...")
synthesizer = get_response_synthesizer(
    llm=llm_model, text_qa_template=prompt, streaming=True)
start_gen = time.time()
response = synthesizer.synthesize(query_str, nodes)
end_gen = time.time()

print("-" * 30)
# print(f"RESPUESTA: {response}")
response.print_response_stream()
print("-" * 30)
print(f"Tiempo real del LLM: {end_gen - start_gen:.4f} seg")
