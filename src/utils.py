from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import TextLoader
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter

from src.log import logger
from src.exceptions import CustomException
import os


# Load all the Python files, excluding venv, returning all as a list
def load_split_git_url(root_URL):
    docs = []

    for dirpath, dirnames, filenames in os.walk(root_URL):
        for file in filenames:
            if file.endswith('.py') and '/.venv/' not in dirpath:
                try: 
                    loader = TextLoader(os.path.join(dirpath, file), encoding='utf-8')
                    docs.extend(loader.load_and_split())                    
                except Exception as e: 
                    raise CustomException(e)
    logger.info(f"Loaded all {len(docs)} python files, excluding venv, and added to 'docs' list.")

    return docs


# Split docs content into chunks
def split_to_chunks(docs):
    try:
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(docs)
        logger.info("Split the docs content into separate chunks, with the chunk size of 1000.")
    except Exception as e:
        raise CustomException(e)
    
    return texts


# Embed and upload the split chunks onto Deeplake
def embed_upload_chunks(documents, account_name):
    try:
        embeddings = OpenAIEmbeddings()
        DeepLake.from_documents(documents, embeddings, dataset_path=f"hub://{account_name}/langchain-code")
        logger.info(f"Uploaded the embedded text chunks unto hub://{account_name}/langchain-code")
    except Exception as e:
        raise CustomException(e)
    
    



