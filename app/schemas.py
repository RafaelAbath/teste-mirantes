from pydantic import BaseModel

class SaleIn(BaseModel):
    product: str
    quantity: int
    unit_price: float
