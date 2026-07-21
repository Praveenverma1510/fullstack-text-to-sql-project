from pydantic import BaseModel
from typing import Any


class DatabaseOut(BaseModel):
    id: int
    name: str
    filename: str
    schema_name: str
    metadata_json: dict[str, Any]

    class Config:
        from_attributes = True


class GenerateSQLIn(BaseModel):
    database_id: int
    question: str


class ExecuteQueryIn(BaseModel):
    database_id: int
    question: str
    sql: str
    limit: int = 100
