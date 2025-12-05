from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class Operator(Base):
    __tablename__ = "operators"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    active_status = Column(Boolean, default=True)
    workload = Column(Integer, default=5)
    create_time = Column(DateTime, default=datetime.utcnow)

    weights = relationship("OperatorWeight", back_populates="operator")
    contacts = relationship("Contact", back_populates="operator")

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    unique_id = Column(String, nullable=False)
    create_time = Column(DateTime, default=datetime.utcnow)

    contacts = relationship("Contact", back_populates="lead")

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    source_name = Column(String, nullable=False)
    create_time = Column(DateTime, default=datetime.utcnow)

    weights = relationship("OperatorWeight", back_populates="source")
    contacts = relationship("Contact", back_populates="source")


class OperatorWeight(Base):
    __tablename__ = "operator_weights"

    id = Column(Integer, primary_key=True, index=True)

    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)
    operator_id = Column(Integer, ForeignKey("operators.id"), nullable=False)
    weight = Column(Integer, default=10)

    source = relationship("Source", back_populates="weights")
    operator = relationship("Operator", back_populates="weights")


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)

    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)
    operator_id = Column(Integer, ForeignKey("operators.id"), nullable=True)

    create_time = Column(DateTime, default=datetime.utcnow)

    lead = relationship("Lead", back_populates="contacts")
    source = relationship("Source", back_populates="contacts")
    operator = relationship("Operator", back_populates="contacts")
