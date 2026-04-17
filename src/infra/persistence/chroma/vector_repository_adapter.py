import chromadb
import time
import logging
from typing import List

from llama_index.core import VectorStoreIndex, QueryBundle, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.ollama import OllamaEmbedding

from src.domain.port import VectorRepository

# Configuración de logs para ver qué pasa internamente
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChromaVectorRepositoryAdapter(VectorRepository):

    def __init__(self, host: str, port: int, collection_name: str, embed_model):

        # 2. Conectar a ChromaDB
        logger.info(f"Conectando a ChromaDB en {host}:{port}...")
        self.client = chromadb.HttpClient(host=host, port=port)

        # 3. Obtener la colección (el objeto, no el string)
        self.collection = self.client.get_collection(collection_name)

        # 4. Configurar el Vector Store y el Storage Context
        self.vector_store = ChromaVectorStore(
            chroma_collection=self.collection)
        self.storage_context = StorageContext.from_defaults(
            vector_store=self.vector_store)

        # 5. Inicializar el índice (esto permite búsquedas rápidas después)
        self.index = VectorStoreIndex.from_vector_store(
            vector_store=self.vector_store,
            embed_model=embed_model
        )

        # 6. Crear el retriever
        self.retriever = self.index.as_retriever(similarity_top_k=3)

        logger.info(
            f"Adaptador ChromaDB inicializado con la colección: {collection_name}")

    def search_relevant_context(self, query: str) -> list:
        """
        Realiza la búsqueda utilizando los componentes ya inicializados.
        """
        if not query:
            return []

        try:
            logger.info(f"Realizando búsqueda en ChromaDB: {query[:50]}...")

            start_ret = time.time()

            # Ejecutar la búsqueda
            nodes = self.retriever.retrieve(QueryBundle(query_str=query))

            end_ret = time.time()

            logger.info(f"Nodos recuperados: {len(nodes)}")
            logger.info(f"Tiempo de búsqueda: {end_ret - start_ret:.4f} seg")

            return nodes

        except Exception as e:
            logger.error(f"Error durante la búsqueda en ChromaDB: {e}")
            return []
