from typing import TypeVar, Generic, Type, Optional, List
from sqlalchemy.orm import Session

# Generic type for any SQLAlchemy model
T = TypeVar('T')

class BaseRepository(Generic[T]):

  def __init__(self, session: Session, model: Type[T]):
    self.session = session
    self.model = model

  def insert(self, entity: T) -> T:
    """Add a new record to the database."""
    self.session.add(entity)
    self.session.commit()
    self.session.refresh(entity)
    return entity

  def get_by_id(self, id: int) -> Optional[T]:
    """Retrieve a record by its primary key."""
    return self.session.query(self.model).get(id)

  def update(self, id: int, **kwargs) -> Optional[T]:
    """Update specific fields of an existing record."""
    obj = self.get_by_id(id)
    if obj:
        for key, value in kwargs.items():
            setattr(obj, key, value)
        self.session.commit()
        self.session.refresh(obj)
    return obj

  def delete(self, id: int) -> bool:
    """Remove a record by its ID."""
    obj = self.get_by_id(id)
    if obj:
        self.session.delete(obj)
        self.session.commit()
        return True
    return False

# Assuming 'session' is your SQLAlchemy Session object
# user_repo = BaseRepository(session, User)
# product_repo = BaseRepository(session, Product)

# 1. Insert
  # new_user = user_repo.insert(User(name="Alice"))
  # new_product = product_repo.insert(Product(price=100))

# 2. Update
  # user_repo.update(new_user.id, name="Alice Smith")

# 3. Delete
  # product_repo.delete(new_product.id)
