import uuid
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.database import UploadedDatabase


class SchemaService:
    def __init__(self, db: Session):
        self.db = db

    def ingest_sql_upload(self, name: str, filename: str, content: bytes):
        if len(content) > settings.max_upload_mb * 1024 * 1024:
            raise ValueError("File too large")

        sql_text = content.decode("utf-8", errors="ignore")
        schema_name = f"ws_{uuid.uuid4().hex[:12]}"

        self.db.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema_name}"'))
        self.db.execute(text(f'SET search_path TO "{schema_name}", public'))
        for stmt in [s.strip() for s in sql_text.split(";") if s.strip()]:
            self.db.execute(text(stmt))

        metadata = self._extract_metadata(schema_name)
        record = UploadedDatabase(
            name=name,
            filename=filename,
            schema_name=schema_name,
            metadata_json=metadata,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def _extract_metadata(self, schema_name: str) -> dict:
        tables = (
            self.db.execute(
                text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = :schema_name
                  AND table_type = 'BASE TABLE'
                ORDER BY table_name
            """),
                {"schema_name": schema_name},
            )
            .mappings()
            .all()
        )

        result = []
        for row in tables:
            table_name = row["table_name"]
            columns = (
                self.db.execute(
                    text("""
                    SELECT column_name, data_type, is_nullable
                    FROM information_schema.columns
                    WHERE table_schema = :schema_name
                      AND table_name = :table_name
                    ORDER BY ordinal_position
                """),
                    {"schema_name": schema_name, "table_name": table_name},
                )
                .mappings()
                .all()
            )
            result.append({"table": table_name, "columns": [dict(c) for c in columns]})

        return {"schema_name": schema_name, "tables": result}
