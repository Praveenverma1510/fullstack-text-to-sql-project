import time
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.ai.text_to_sql import TextToSQLService
from app.models.database import QueryHistory, UploadedDatabase
from app.utils.sql_guard import validate_read_only_sql


class QueryService:
    def __init__(self, db: Session):
        self.db = db
        self.generator = TextToSQLService()

    def generate_sql(self, database_id: int, question: str):
        record = self.db.query(UploadedDatabase).filter_by(id=database_id).first()
        if not record:
            raise ValueError("Database not found")

        schema_lines = []
        for table in record.metadata_json.get("tables", []):
            cols = ", ".join(
                f"{c['column_name']} {c['data_type']}" for c in table.get("columns", [])
            )
            schema_lines.append(f"Table {table['table']} ({cols})")

        generated = self.generator.generate(question, "\n".join(schema_lines))

        print("========== GENERATED ==========")
        print(generated)
        print("===============================")
        ok, error = validate_read_only_sql(generated["sql"])
        if not ok:
            generated["sql"] = "SELECT 1 WHERE FALSE;"
            generated["explanation"] += f" Rejected by validator: {error}"
        return generated

    def execute_query(
        self, database_id: int, question: str, sql: str, limit: int = 100
    ):
        record = self.db.query(UploadedDatabase).filter_by(id=database_id).first()
        if not record:
            raise ValueError("Database not found")

        ok, error = validate_read_only_sql(sql)
        if not ok:
            self._save_history(database_id, question, sql, 0, False, error)
            return {"success": False, "error_message": error, "rows": [], "columns": []}

        start = time.perf_counter()
        conn = self.db.connection()
        conn.execute(text(f'SET search_path TO "{record.schema_name}"'))
        conn.execute(text("SET statement_timeout TO 5000"))
        result = conn.execute(text(sql))
        rows = [dict(r._mapping) for r in result.fetchmany(limit)]
        execution_time_ms = int((time.perf_counter() - start) * 1000)
        self._save_history(database_id, question, sql, execution_time_ms, True, None)

        return {
            "success": True,
            "generated_sql": sql,
            "columns": list(rows[0].keys()) if rows else list(result.keys()),
            "rows": rows,
            "row_count": len(rows),
            "execution_time_ms": execution_time_ms,
        }

    def _save_history(
        self, database_id, question, sql, execution_time_ms, success, error_message
    ):
        entry = QueryHistory(
            database_id=database_id,
            question=question,
            generated_sql=sql,
            execution_time_ms=execution_time_ms,
            success=1 if success else 0,
            error_message=error_message,
        )
        self.db.add(entry)
        self.db.commit()
