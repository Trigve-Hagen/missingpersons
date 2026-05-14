import shutil
import os
from flask import flash
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import mimetypes
mimetypes.add_type('text/x-python', '.py')

class CodeLoader():
  def __init__(self):
    self.base_path = os.path.abspath(".")
    self.code_optimize_directory = os.path.join(self.base_path, "database\\code_optimize_db")

  def delete_code_chroma(self):
    try:
      shutil.rmtree(self.code_optimize_directory)
      flash(f"{self.code_optimize_directory} removed successfully!", "success")
    except Exception as e:
      flash(f"Error deleting {self.code_optimize_directory}: {e}", "danger")
      return False

  def ingest_python_repo(self):
    # 1. Load Python files from the directory
    # LanguageParser automatically identifies code structures
    # fileTypes = [".py", ".html", ".css", ".js", ".txt"]
    # for type in fileTypes:
    loader = DirectoryLoader(
        self.base_path,
        glob="**/*.py",
        loader_cls=TextLoader,
        loader_kwargs={'encoding': 'utf-8'}
    )
    documents = loader.load()
    print(f"Loaded {len(documents)} files from {self.base_path}")

    # 2. Split code into meaningful chunks
    # Using the Python-specific splitter helps keep functions/classes together
    # if type == ".py":
    code_splitter = RecursiveCharacterTextSplitter.from_language(
      language=Language.PYTHON,
      chunk_size=1000,
      chunk_overlap=100
    )
    # else:
    #   code_splitter = RecursiveCharacterTextSplitter.from_language(
    #     chunk_size=1000,
    #     chunk_overlap=100
    #   )

    texts = code_splitter.split_documents(documents)
    flash(f"Split into {len(texts)} chunks")

    # 3. Initialize HuggingFace Embeddings
    # 'all-MiniLM-L6-v2' is a fast, lightweight open-source model
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'} # Change to 'cuda' if GPU is available
    )

    # 4. Create and persist the Chroma DB
    vector_db = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=self.code_optimize_directory
    )
    flash(f"Files persisted to {self.code_optimize_directory}")
    return vector_db
