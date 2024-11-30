from langchain_community.document_loaders.pdf import PyMuPDFLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings.openai import OpenAIEmbeddings
import chromadb
from functools import cache
import os

import uuid

import chromadb
from chromadb.config import Settings


def load_pdf(file_path):
    if not file_path.endswith('.pdf'):
        return False

    loader = PyMuPDFLoader(file_path)
    return loader.load()


def read_docx(file_path):
    loader = UnstructuredWordDocumentLoader(
        file_path, mode="single", strategy="fast")
    return loader.load()


def splitter(txt):
    chunk_size = 1000
    chunk_overlap = 200

    def length_function(text: str) -> int:
        return len(text)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=length_function
    )

    return splitter.split_documents(txt)


@cache
def encode(model_id="", device="", use_open_ai=False):
    if use_open_ai:
        opena_api_key = os.getenv('OPENAI_API_KEY')
        return OpenAIEmbeddings(openai_api_key=opena_api_key, model="text-embedding-3-small")
    else:
        return HuggingFaceEmbeddings(model_name=model_id, model_kwargs={"device": device})


def load_and_embedd(file_paths, embeddings, name, is_json=False):

    docs = []
    for file_path in file_paths:
        if file_path.endswith('.pdf'):
            documents = load_pdf(file_path)
            splitted_txt = splitter(documents)
        elif file_path.endswith('.docs'):
            documents = read_docx(file_path)
            splitted_txt = splitter(documents)
        else:
            continue
        
        docs.extend(splitted_txt)

    client = chromadb.PersistentClient(path='store')

    try:
        client.get_collection(name=name)
        print('allready exist')
        vector_db = Chroma(client=client, collection_name=name, embedding_function=embeddings)
        
    except:
        client.get_or_create_collection(name=name)
        vector_db = Chroma.from_documents(
            documents=docs,
            embedding=embeddings,
            client=client,
            collection_name=name
        )
 
    return vector_db
