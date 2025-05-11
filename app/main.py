import os
from fastapi import FastAPI, File, UploadFile, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.responses import StreamingResponse

from .models import Base
from .crud   import create_sale, get_report
from .utils  import parse_csv
from .utils  import generate_report_pdf

DATABASE_URL = os.getenv("DATABASE_URL")  # string do Supabase

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sales Report API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload_csv")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    sales = parse_csv(await file.read())
    for s in sales:
        create_sale(db, s)
    return {"inserted": len(sales)}

@app.get("/report")
def report(db: Session = Depends(get_db)):
    rows, overall, best = get_report(db)
    return {
        "per_product": [
            {"product": r.product,
             "quantity": int(r.total_qty),
             "total_value": float(r.total_value)} for r in rows
        ],
        "best_seller": best,
        "overall": overall
    }
@app.get("/report/pdf", response_class=StreamingResponse)
def report_pdf(db: Session = Depends(get_db)):
    
    rows, overall, best = get_report(db)
    
    pdf_io = generate_report_pdf(
        [(r.product, r.total_qty, r.total_value) for r in rows],
        overall,
        best
    )
    
    return StreamingResponse(
        pdf_io,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=relatorio_vendas.pdf"}
    )
