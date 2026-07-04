# Agente Inteligente - Santos Pegasus Soluciones

Agente de inteligencia artificial que responde preguntas sobre la Guía Oficial de Ingeniería Back-end de Santos Pegasus Soluciones, una empresa ficticia de tecnología especializada en microservicios e IA.

Este proyecto fue desarrollado como parte del Challenge Alura Agente.

## Descripción del proyecto

El agente lee un documento PDF con las normas técnicas de ingeniería back-end de la empresa y permite hacer preguntas en lenguaje natural sobre su contenido, devolviendo respuestas basadas únicamente en la información del documento.

## Arquitectura

El proyecto sigue una arquitectura RAG (Retrieval-Augmented Generation):

1. **Carga del documento**: se lee el PDF usando PyPDFLoader.
2. **División en fragmentos**: el texto se divide en fragmentos de 1000 caracteres con 200 de superposición, usando RecursiveCharacterTextSplitter.
3. **Generación de embeddings**: cada fragmento se convierte en un vector numérico con el modelo gemini-embedding-001 de Google.
4. **Almacenamiento vectorial**: los vectores se guardan en una base FAISS para poder buscar los fragmentos más relevantes según la pregunta.
5. **Generación de respuesta**: al recibir una pregunta, se buscan los fragmentos más relevantes y se le pasan como contexto al modelo gemini-2.5-flash, que genera la respuesta final.

## Tecnologías utilizadas

- Python
- LangChain
- FAISS (faiss-cpu)
- Google Gemini API (gemini-embedding-001 y gemini-2.5-flash)
- python-dotenv

## Estructura del proyecto