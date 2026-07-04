import os
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

RUTA_DOCUMENTO = "documentos/santo pegasus.pdf"


def cargar_documento(ruta):
    loader = PyPDFLoader(ruta)
    return loader.load()


def dividir_documento(documento):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_documents(documento)


def crear_vectorstore(fragmentos):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key=GEMINI_API_KEY)
    vectorstore = None
    for fragmento in fragmentos:
        if vectorstore is None:
            vectorstore = FAISS.from_documents([fragmento], embeddings)
        else:
            vectorstore.add_documents([fragmento])
        time.sleep(2)
    return vectorstore


def crear_agente(vectorstore):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GEMINI_API_KEY)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    def preguntar(pregunta):
        documentos_relevantes = retriever.invoke(pregunta)
        contexto = "\n\n".join([doc.page_content for doc in documentos_relevantes])
        prompt = f"Responde la siguiente pregunta basandote unicamente en el contexto proporcionado.\n\nContexto:\n{contexto}\n\nPregunta: {pregunta}"
        respuesta = llm.invoke(prompt)
        return respuesta.content

    return preguntar


def main():
    documento = cargar_documento(RUTA_DOCUMENTO)
    fragmentos = dividir_documento(documento)
    vectorstore = crear_vectorstore(fragmentos)
    preguntar = crear_agente(vectorstore)

    print("Agente listo. Escribe una pregunta (o 'salir' para terminar).")
    while True:
        pregunta = input("\nPregunta: ").strip()
        if pregunta.lower() == "salir":
            break
        if pregunta == "":
            continue
        respuesta = preguntar(pregunta)
        print(respuesta)


if __name__ == "__main__":
    main()