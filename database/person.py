# https://www.youtube.com/watch?v=AKQ3XEDI9Mw
# schema - person - person of interest - id, iid, ifMissing - missing or POI, ssn, gender, dob

from sqlalchemy import ForeignKey, Column, String, Integer, CHAR, DateTime, Boolean, func
from database.base import Base

class Person(Base):
  __tablename__ = "people"

  id = Column("id", Integer, primary_key=True)
  ifMissing = Column("ifMissing", Boolean, default=True, nullable=False)
  linkedBy = Column("linkedBy", String) # what are they linked by service, email, phone
  height = Column("height", String)
  weight = Column("weight", String)
  hairColor = Column("hairColor", String)
  eyeColor = Column("eyeColor", String)
  ssn = Column("ssn", Integer)
  gender = Column("gender", CHAR)
  dob = Column("dob", DateTime)

  def __init__(self, id, ifMissing, linkedBy, height, weight, hairColor, eyeColor, ssn, gender, dob):
    self.id = id
    self.ifMissing = ifMissing
    self.linkedBy = linkedBy
    self.height = height
    self.weight = weight
    self.hairColor = hairColor
    self.eyeColor = eyeColor
    self.ssn = ssn
    self.gender = gender
    self.dob = dob

  def __repr__(self):
    return f"({self.id}) {self.ifMissing} {self.linkedBy} {self.height} {self.weight} {self.hairColor} {self.eyeColor} {self.ssn} ({self.gender}, {self.dob})"

class Name(Base):
  __tablename__ = "names"

  id = Column("id", Integer, primary_key=True)
  ifAlias = Column("ifAlias", Boolean, default=False, nullable=False)
  fullName = Column("fullName", String) # define name as first middle last for separation
  sirName = Column("sirName", String)
  owner = Column(Integer, ForeignKey("people.id"))

  def __init__(self, id, ifAlias, fullName, sirName, owner):
    self.id = id
    self.ifAlias = ifAlias
    self.sirName = sirName
    self.fullName = fullName
    self.owner = owner

  def __repr__(self):
    return f"({self.id}) {self.ifAlias} {self.sirName} {self.fullName} owned by {self.owner}"

  def validate():
    pass

class Email(Base):
  __tablename__ = "emails"

  id = Column("id", Integer, primary_key=True)
  email = Column(String(255), unique=True, nullable=False)
  owner = Column(Integer, ForeignKey("people.id"))

  def __init__(self, id, email, owner):
    self.id = id
    self.email = email
    self.owner = owner

  def __repr__(self):
    return f"({self.id}) {self.email} owned by {self.owner}"

  def validate():
    pass

class Phone(Base):
  __tablename__ = "phones"

  id = Column("id", Integer, primary_key=True)
  phone = Column(String(20), unique=True, nullable=False)
  owner = Column(Integer, ForeignKey("people.id"))

  def __init__(self, id, phone, owner):
    self.id = id
    self.phone = phone
    self.owner = owner

  def __repr__(self):
    return f"({self.id}) {self.phone} owned by {self.owner}"

  def validate():
    pass

class Address(Base):
  __tablename__ = "addresses"

  id = Column("id", Integer, primary_key=True)
  address1 = Column("address1", String)
  address2 = Column("address2", String)
  city = Column("city", String)
  state = Column("state", String)
  zip5 = Column("zip5", Integer)
  zip4 = Column("zip4", Integer)
  owner = Column(Integer, ForeignKey("people.id"))

  def __init__(self, id, address1, address2, city, state, zip5, zip4, owner):
    self.id = id
    self.address1 = address1
    self.address2 = address2
    self.city = city
    self.state = state
    self.zip5 = zip5
    self.zip4 = zip4
    self.owner = owner

  def __repr__(self):
    return f"({self.id}) {self.address1} {self.address2} {self.city} {self.state} {self.zip5} {self.zip4} owned by {self.owner}"

  def validate():
    pass
