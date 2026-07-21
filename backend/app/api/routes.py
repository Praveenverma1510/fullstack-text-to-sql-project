from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.session import Base, engine, get_db
from app.models.database import QueryHistory, UploadedDatabase
from app.schemas.database import ExecuteQueryIn, GenerateSQLIn
from app.services.query_service import QueryService
from app.services.schema_service import SchemaService

# Base.metadata.create_all(bind=engine)
router = APIRouter()


@router.get("/schema")
def get_schema(db: Session = Depends(get_db)):
    rows = db.query(UploadedDatabase).order_by(UploadedDatabase.created_at.desc()).all()
    return [
        {
            "id": r.id,
            "name": r.name,
            "filename": r.filename,
            "schema_name": r.schema_name,
            "metadata_json": r.metadata_json,
        }
        for r in rows
    ]


@router.post("/upload")
async def upload_sql(
    name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename.lower().endswith(".sql"):
        raise HTTPException(status_code=400, detail="Only .sql files are allowed")
    content = await file.read()
    service = SchemaService(db)
    try:
        record = service.ingest_sql_upload(
            name=name, filename=file.filename, content=content
        )
        return {
            "id": record.id,
            "name": record.name,
            "filename": record.filename,
            "schema_name": record.schema_name,
            "tables": record.metadata_json.get("tables", []),
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/generate-sql")
def generate_sql(payload: GenerateSQLIn, db: Session = Depends(get_db)):
    try:
        service = QueryService(db)
        result = service.generate_sql(payload.database_id, payload.question)
        return {"generated_sql": result["sql"], "explanation": result["explanation"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/execute-query")
def execute_query(payload: ExecuteQueryIn, db: Session = Depends(get_db)):
    try:
        service = QueryService(db)
        return service.execute_query(
            payload.database_id, payload.question, payload.sql, payload.limit
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/history")
def history(db: Session = Depends(get_db)):
    rows = (
        db.query(QueryHistory).order_by(QueryHistory.created_at.desc()).limit(100).all()
    )
    return [
        {
            "id": r.id,
            "database_id": r.database_id,
            "question": r.question,
            "generated_sql": r.generated_sql,
            "execution_time_ms": r.execution_time_ms,
            "success": bool(r.success),
            "error_message": r.error_message,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in rows
    ]


@router.get("/tables/{database_id}")
def tables(database_id: int, db: Session = Depends(get_db)):
    row = db.query(UploadedDatabase).filter_by(id=database_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Database not found")
    return row.metadata_json.get("tables", [])
