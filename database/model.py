from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, DateTime, Boolean, func, Text
from database.base import Base, NullToEmptyString # Import shared base

class Model(Base):
  __tablename__ = "models"

  id = Column("id", Integer, primary_key=True)
  name = Column(NullToEmptyString)
  model = Column(NullToEmptyString)
  type = Column(NullToEmptyString, default="ollama")

  def __init__(self, name, model, type, system):
    self.name = name # instance
    self.model = model # model
    self.type = type  # from

class ModelParams(Base):
  __tablename__ = "model_params"

  id = Column("id", Integer, primary_key=True)
  name = Column(NullToEmptyString)
  value = Column(NullToEmptyString)
  owner = Column(Integer, ForeignKey("models.id"))

  def __init__(self, name, value, owner):
    self.name = name
    self.value = value
    self.owner = owner

class Prompt(Base):
  __tablename__ = "prompts"

  id = Column("id", Integer, primary_key=True)
  prompt = Column(Text)

  def __init__(self, prompt):
    self.prompt = prompt

class Question(Base):
  __tablename__ = "questions"

  id = Column("id", Integer, primary_key=True)
  question = Column(Text)

  def __init__(self, question):
    self.question = question
