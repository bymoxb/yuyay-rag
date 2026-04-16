import chromadb
import re

from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.readers.docling import DoclingReader
from llama_index.embeddings.ollama import OllamaEmbedding
from embed_model import embed_model_name, collection_name
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core.schema import TextNode


# PASO 1: Configurar el modelo de Embedding
# Esto es vital. Todos los documentos se convertirán a vectores usando este modelo.
Settings.embed_model = OllamaEmbedding(model_name=embed_model_name)

# PASO 2: Conectar con tu instancia de Chroma en ejecución
# Ajusta host y port según tu configuración (ej. localhost:8000)
chroma_client = chromadb.HttpClient(host='localhost', port=8000)

# IMPORTANTE: Limpiar la colección antes de insertar nuevos datos (opcional, pero recomendado para pruebas)
chroma_client.delete_collection(name=collection_name)

# Crear (o recuperar) la colección donde se guardarán los datos
chroma_collection = chroma_client.get_or_create_collection(collection_name)


# PASO 3: Configurar el almacenamiento (Storage Context)
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# PASO 4: Cargar documentos con Docling y guardarlos en Chroma


def simple_node_parser(documents):
    parser = SimpleNodeParser.from_defaults(
        chunk_size=800,
        chunk_overlap=100
    )

    nodes = parser.get_nodes_from_documents(documents)

    # Necesito guardar los nodos en un directorio y cada nodo en un archivo en texto plano
    for i, node in enumerate(nodes):
        with open(f"store/nodo_{i}.txt", "w", encoding="utf-8") as f:
            f.write(node.get_content())

    return nodes


def chunk_section(section, max_len=1000):
    texto = f"{section['titulo']}\n{section['contenido']}"

    if len(texto) <= max_len:
        return [texto]

    # dividir por párrafos
    partes = texto.split("\n\n")

    chunks = []
    actual = ""

    for p in partes:
        if len(actual) + len(p) < max_len:
            actual += "\n\n" + p
        else:
            chunks.append(actual.strip())
            actual = p

    if actual:
        chunks.append(actual.strip())

    return chunks


def section_markdown_parser(markdown_text) -> list[TextNode]:
    sections = re.split(r'(## .+)', markdown_text)

    resultado = []
    for i in range(1, len(sections), 2):
        titulo = sections[i]
        contenido = sections[i+1] if i+1 < len(sections) else ""

        resultado.append({
            "titulo": titulo.strip(),
            "contenido": contenido.strip()
        })

    nodes = []

    for i, seccion in enumerate(resultado):
        chunks = chunk_section(seccion, float('inf'))

        for j, chunk in enumerate(chunks):
            # node_id = f"nodo_{i}_{j}"
            nodes.append(TextNode(
                text=chunk,
                metadata={
                    "seccion": seccion["titulo"],
                    # "documento": "nombre.pdf"
                }
            ))

    for i, seccion in enumerate(resultado):
        with open(f"cache/markdown/nodo_{i}.txt", "w", encoding="utf-8") as f:
            f.write(f"{seccion['titulo']}\n\n{seccion['contenido']}")

    return nodes


def cargar_y_guardar(ruta_pdf):
    # 1. Leer el PDF (esto usa los modelos de IBM Docling)
    print(f"Cargando documento desde: {ruta_pdf}")
    reader = DoclingReader()
    documents = reader.load_data(file_path=ruta_pdf)

    # nodes = simple_node_parser(documents)
    nodes = section_markdown_parser(documents[0].get_content())

    print(f"Documento cargado. Número de nodos creados: {len(nodes)}")

    # 2. Crear el índice
    # Al pasarle el 'storage_context', LlamaIndex sabe que NO debe guardarlo
    # en memoria, sino enviarlo directamente a tu instancia de Chroma.
    print("Creando índice y guardando en Chroma...")
    index = VectorStoreIndex(
        nodes=[],
        storage_context=storage_context,
        show_progress=True,
    )

    success = 0
    fails = 0

    for i, node in enumerate(nodes):
        try:
            index.insert_nodes([node])
            success += 1
        except Exception as e:
            print(f"Error en nodo {i}. Error: {str(e)}")
            fails += 1

    print(f"Índice creado. Nodos insertados: {success}. Fallos: {fails}.")
    print(f"Éxito: Documento {ruta_pdf} guardado en Chroma.")

    return index


# Ejecución
if __name__ == "__main__":
    mi_archivo = "store/FICHA TECNICA COMPROBANTES ELECTRO_NICOS offline.pdf"
    index = cargar_y_guardar(mi_archivo)
