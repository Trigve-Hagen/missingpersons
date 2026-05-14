from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, DateTime, Boolean, func, CheckConstraint, Text
from database.base import Base, NullToEmptyString # Import shared base

class State(Base):
  __tablename__ = 'state'
  __table_args__ = (
    CheckConstraint('id = 1', name='only_one_row'),
  )

  id = Column(Integer, primary_key=True, default=1)
  person = Column(Integer, default=0)
  model = Column(Integer, default=0)
  api = Column(Integer, default=0)
  prompt = Column(Integer, default=0)
  question = Column(Integer, default=0)
  processor = Column(NullToEmptyString, default="cpu")
  root_node = Column(NullToEmptyString, default="")
  files_size = Column(Integer, default=0)
  sql_alchemy_database_size = Column(Integer, default=0)
  chroma_database_size = Column(Integer, default=0)
  ollama_models_size = Column(Integer, default=0)
  display_type = Column(NullToEmptyString, default="")

class Notice(Base):
  __tablename__ = "notices"

  id = Column("id", Integer, primary_key=True)
  type = Column(NullToEmptyString)
  title = Column(NullToEmptyString)
  description = Column(NullToEmptyString)
  ifComplete = Column(Integer, default=0)
  dateCreated = Column(DateTime, server_default=func.now())

  def __init__(self, type, title, description, ifComplete):
    self.type = type
    self.title = title
    self.description = description
    self.ifComplete = ifComplete
