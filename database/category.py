# schema - category - Id, type, name
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, DateTime, Boolean, func
from database.base import Base # Import shared base

class Category(Base):
  __tablename__ = "categories"

  id = Column("id", Integer, primary_key=True)
  type = Column(String(20)) # contactType
  name = Column(String(255), unique=True, nullable=False)

  def __init__(self, type, name):
    self.type = type
    self.name = name

  def __repr__(self):
    return f"({self.id}) {self.type} {self.name}"

  def validate():
    pass
