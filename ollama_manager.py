import os
import re
import platform
import ollama
from flask import flash
from sqlalchemy import create_engine, inspect, exc, select, update
from database.state import State
from database.model import Model
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_classic.chains.retrieval_qa.base import RetrievalQA
from pydantic import BaseModel, Field
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

class TaskSuggestion(BaseModel):
    title: str = Field(description="Short title of the task")
    description: str = Field(description="Detailed steps or context for the task")

class TaskList(BaseModel):
    suggestions: List[TaskSuggestion] = Field(description="List of exactly 10 task suggestions")

class OllamaManager:
  def __init__(self, session):
    self.session = session
    self.client = ollama.Client()
    self.base_path = os.path.abspath(".")
    self.investigation_directory = os.path.join(self.base_path, "database\\chroma_db")
    # self.investigation_optimize_directory = os.path.join(self.base_path, "database\\investigation_optimize_db")
    self.code_optimize_directory = os.path.join(self.base_path, "database\\code_optimize_db")
    self.collection_name = "missing_persons"
    self.model_name = "phi3:mini"

  def initialize():
    pass

  def prompt(self):
    state = self.session.execute(select(State).filter_by(id = 1)).scalar_one_or_none()
    model = self.session.execute(select(Model).filter_by(id = state.model)).scalar_one_or_none()

    if model:
      try:
        # --- Initialize LangChain Components ---
        # Load HuggingFace Embeddings
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # Load existing Chroma collection
        if os.path.exists(self.self.investigation_directory):
            vectorstore = Chroma(
                persist_directory=self.self.investigation_directory,
                embedding_function=embeddings,
                collection_name=self.collection_name
            )
        else:
            # raise ValueError(f"Chroma collection not found at {self.self.investigation_directory}")
            flash(f"Chroma collection not found at {self.self.investigation_directory}", "danger")
            return False

        # Create Retriever
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

        # Initialize Ollama model
        llm = ChatOllama(model=model.model)

        try:
          # Create Chain
          qa_chain = RetrievalQA.from_chain_type(
              llm=llm,
              chain_type="stuff",
              retriever=retriever,
              return_source_documents=False
          )
          return qa_chain
        except Exception as e:
          flash(f"Error fetching chain: {e}", "danger")
          return False
      except Exception as e:
        flash(f"Error prompting models: {e}", "danger")
        return False
    else:
      flash(f"Error fetching models: Please set a model.", "danger")
      return False

  def suggestions(self, type='code'):
    model = "deepseek-coder-v2"
    if type == 'code':
      selected_directory = self.code_optimize_directory
    else:
      selected_directory = self.investigation_directory

    if model:
      try:
        # --- Initialize LangChain Components ---
        # Load HuggingFace Embeddings
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # Load existing Chroma collection
        if os.path.exists(selected_directory):
            vectorstore = Chroma(
                persist_directory=selected_directory,
                embedding_function=embeddings,
                collection_name=self.collection_name
            )
        else:
            flash(f"Chroma collection not found at {selected_directory}", "danger")
            return False

        # Create Retriever
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

        # Initialize Ollama model
        llm = ChatOllama(model=model, format="json", temperature=0.7)

        parser = PydanticOutputParser(pydantic_object=TaskList)
        if type == 'code':
          prompt = ChatPromptTemplate.from_template(
            "Act as an expert software optimizer. The code in the following context is a flask application that uses data from form uploads and external sources combined with AI to aid in the search for missing persons. The external data comes from APIs, RSS feeds and uploaded data including text, images and documents. The application is coverted to a console application using pywebview. The application needs to be as versatile as possible. Analyze the following code context and provide 10 specific, actionable suggestions to improve performance, readability, versatility, or security.\n"
            "Context: {context}\n"
            "User Request: {query}\n"
            "{format_instructions}"
          )
          query = "Suggest 10 changes I could do to the code base to optimize it."
        else:
          prompt = ChatPromptTemplate.from_template(
            "Act as an expert investigator. Analyze the following investigation context and provide 10 specific, actionable suggestions to improve the chances of finding the missing person and the person or persons responsible.\n"
            "Context: {context}\n"
            "User Request: {query}\n"
            "{format_instructions}"
          )
          query = "Suggest 10 changes I could make to the investigation to optimize it."

        try:
          # 4. Execute Chain
          context_docs = retriever.invoke(query)
          context_text = "\n".join([doc.page_content for doc in context_docs])
          chain = prompt | llm | parser
          response = chain.invoke({
              "context": context_text,
              "query": query,
              "format_instructions": parser.get_format_instructions()
          })
          return response
        except Exception as e:
          flash(f"Error fetching chain: {e}", "danger")
          return False
      except Exception as e:
        flash(f"Error prompting models: {e}", "danger")
        return False
    else:
      flash(f"Error fetching models: Please set a model.", "danger")
      return False

  def get_models(self):
    """Lists all locally downloaded models."""
    models = []
    try:
      models = self.client.list()
    except Exception as e:
      flash(f"Error fetching models: {e}", "danger")

    return models

  def is_model_downloaded(self, name):
    # checks if the model is downloaded already.
    local_models = ollama.list()
    for model in local_models['models']:
      if model['model'] == name:
        return True
    return False

  def download_model(self, model_name: str):
    # Downloads/Pulls an Ollama model.
    try:
      ollama.pull(model_name)
      flash(f"Model {model_name} downloaded successfully.", "success")
      return True
    except ollama.ResponseError as e:
      if "404" in str(e):
        flash(f"Model '{model_name}' does not exist on ollama.com.", "danger")
      else:
        flash(f"An error occurred: {e}", "danger")
      return False
    except Exception as e:
      flash(f"Error fetching models: {e}", "danger")
      return False

  def create_machine_name(self, text):
    text = text.lower()
    text = re.sub(r'[\s\-]+', '_', text)
    text = re.sub(r'[^\w]', '', text)
    return text.strip('_')

  def create_model(self, model: Model, parameters):
    try:
      ollama.create(
          model=self.create_machine_name(model.name),
          from_=model.model,
          system=model.system,
          parameters=parameters
      )
      flash(f"Model {model.name} created successfully.", "success")
      return True
    except Exception as e:
      flash(f"Error creating model: {e}", "danger")
      return False

  def stop_model(self, model_name: str):
    """Stops/Unloads a model from memory."""
    print(f"Stopping {model_name}...")
    # Setting keep_alive=0 purges the model from memory
    self.client.generate(model_name, keep_alive=0)
    print(f"Model {model_name} stopped.")

  def remove_model(self, model_name: str):
    """Removes a model from the system."""
    try:
      self.client.delete(model_name)
      flash(f"Model {model_name} removed.", "success")
      return True
    except Exception as e:
      flash(f"Error removing model: {e}", "danger")
      return False

  def get_ollama_storage_gb(self):
    """ Returns the total size of Ollama's model storage in Gigabytes. """
    # Determine default path based on OS
    home = os.path.expanduser("~")
    system = platform.system()

    if system == "Windows":
      path = os.path.join(home, ".ollama", "models")
    elif system == "Darwin":  # macOS
      path = os.path.join(home, ".ollama", "models")
    else:  # Linux (standard default)
      path = "/usr/share/ollama/.ollama/models"
      if not os.path.exists(path):
        path = os.path.join(home, ".ollama", "models")

    # If the user has set a custom path via OLLAMA_MODELS, use that instead
    path = os.environ.get("OLLAMA_MODELS", path)

    if not os.path.exists(path):
      return 0.0

    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
      for f in filenames:
        fp = os.path.join(dirpath, f)
        # skip if it is a symbolic link
        if not os.path.islink(fp):
          total_size += os.path.getsize(fp)

    # Convert bytes to Gigabytes
    return total_size / (1024**3)

# --- Usage Example ---
# manager = OllamaManager()

# Example workflow
# manager.download_model("llama3")
# manager.list_models()
# manager.stop_model("llama3")
# manager.remove_model("llama3")
# manager.get_ollama_storage_gb()
