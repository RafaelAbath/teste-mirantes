from sqlalchemy.orm import Session
from .models import Sale
from sqlalchemy import func

def create_sale(db: Session, sale_in):
    sale = Sale(**sale_in.dict())
    db.add(sale)
    db.commit()
    db.refresh(sale)
    return sale

def get_report(db: Session):
    rows = db.query(
        Sale.product,
        func.sum(Sale.quantity).label("total_qty"),
        func.sum(Sale.quantity * Sale.unit_price).label("total_value")
    ).group_by(Sale.product).all()

    overall = sum(r.total_value for r in rows) if rows else 0
    best    = max(rows, key=lambda r: r.total_qty).product if rows else None
    return rows, overall, best
