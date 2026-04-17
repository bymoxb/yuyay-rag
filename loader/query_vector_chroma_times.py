import os
import time
import chromadb
import dotenv

from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.postprocessor import SentenceTransformerRerank, LLMRerank
from llama_index.core import QueryBundle

from embed_model import embed_model_name, collection_name
from prompt import prompt

dotenv.load_dotenv()

WITH_RERANKER = True
VECTOR_TOP_K = 3 if not WITH_RERANKER else 10
RERANKER_TOP_N = 3

MODEL_TIME_OUT = 120

# 1. Configuración
embed_model = OllamaEmbedding(model_name=embed_model_name)


llm_model = Ollama(model="mistral:latest", request_timeout=MODEL_TIME_OUT)
# llm_model = Ollama(model="gemma4:e2b", request_timeout=MODEL_TIME_OUT)
# llm_model = Ollama(model="llama3.1:8b", request_timeout=MODEL_TIME_OUT)
# llm_model = OpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))
# llm_model = OpenAI(model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"))

remote_db = chromadb.HttpClient(host='localhost', port=8000)
chroma_collection = remote_db.get_collection(collection_name)
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store, embed_model=embed_model)

# reranker = LLMRerank(
#     llm=llm_model,
#     top_n=RERANKER_TOP_N,
# )

reranker = SentenceTransformerRerank(
    # model="BAAI/bge-reranker-base",
    model="BAAI/bge-reranker-v2-m3",
    top_n=3
)

query_str = "Hola"
# query_str = "Explicame sobre los nivel de seguridad en la firma electrónica"
# query_str = "Cuales son los motivos de los comprobantes con errores y rechazados que se pueden volver solicitar?"
# query_str = "Cuales son los valores sub totales y totales con impuestos que deben constar en los comprobantes de venta?"

query_bundle = QueryBundle(query_str)

# --- PASO 1: MEDICIÓN DEL EMBEDDING ---
# print("Generando embedding de la consulta...")
# start_emb = time.time()
# query_embedding = embed_model.get_query_embedding(query_str)
# end_emb = time.time()
# print(f"Tiempo solo para generar el vector: {end_emb - start_emb:.4f} seg")

# --- PASO 2: RETRIEVAL (BÚSQUEDA EN CHROMADB) ---
print("Realizando búsqueda en ChromaDB...")
retriever = index.as_retriever(similarity_top_k=VECTOR_TOP_K)
start_ret = time.time()
nodes = retriever.retrieve(str_or_query_bundle=query_bundle)
end_ret = time.time()
print(f"Tiempo de búsqueda en DB: {end_ret - start_ret:.4f} seg")

if WITH_RERANKER:
    print(f"Aplicando reranking a un total de nodos {len(nodes)}")
    start_ret = time.time()
    nodes = reranker.postprocess_nodes(nodes=nodes, query_bundle=query_bundle)
    end_ret = time.time()
    print(f"Tiempo de RERANKER: {end_ret - start_ret:.4f} seg")


# Si esto es 0, por eso la generación es rápida
print(f"Nodos recuperados: {len(nodes)}")

# --- PASO 3: GENERACIÓN (LLM) ---
print("Generando respuesta con LLM...")
synthesizer = get_response_synthesizer(
    llm=llm_model, text_qa_template=prompt, streaming=True)
start_gen = time.time()
response = synthesizer.synthesize(query=query_bundle, nodes=nodes)
end_gen = time.time()

print("-" * 50)
# print(f"RESPUESTA: {response}")
response.print_response_stream()
print("-" * 30)
print(f"Tiempo real del LLM: {end_gen - start_gen:.4f} seg")
