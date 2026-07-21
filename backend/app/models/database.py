from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String, Text, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class UploadedDatabase(Base):
    __tablename__ = "uploaded_databases"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    filename = Column(String(255), nullable=False)
    schema_name = Column(String(255), nullable=False, unique=True)
    metadata_json = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    histories = relationship("QueryHistory", back_populates="database", cascade="all, delete-orphan")


class QueryHistory(Base):
    __tablename__ = "query_history"

    id = Column(Integer, primary_key=True)
    database_id = Column(Integer, ForeignKey("uploaded_databases.id", ondelete="CASCADE"), nullable=False)
    question = Column(Text, nullable=False)
    generated_sql = Column(Text, nullable=False)
    execution_time_ms = Column(Integer)
    success = Column(Integer, default=1)
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    database = relationship("UploadedDatabase", back_populates="histories")
