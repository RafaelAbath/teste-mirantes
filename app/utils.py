import csv
from io import StringIO
from typing import List
from .schemas import SaleIn
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def parse_csv(file_bytes: bytes) -> List[SaleIn]:
    csv_text = file_bytes.decode("utf-8")
    reader = csv.DictReader(StringIO(csv_text))
    return [SaleIn(product=r["produto"],
                   quantity=int(r["quantidade"]),
                   unit_price=float(r["preco_unitario"]))
            for r in reader]
def generate_report_pdf(rows, overall, best_seller) -> BytesIO:
    """
    Monta um PDF em memória com o relatório de vendas.
    'rows' é lista de tuplas (product, total_qty, total_value).
    """
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(width / 2, height - 40, "Relatório de Vendas")

    
    p.setFont("Helvetica-Bold", 12)
    y = height - 80
    p.drawString(50, y, "Produto")
    p.drawString(200, y, "Quantidade")
    p.drawString(330, y, "Total (R$)")
    y -= 20
    p.line(50, y + 10, width - 50, y + 10)


    p.setFont("Helvetica", 12)
    for product, qty, total in rows:
        p.drawString(50, y, str(product))
        p.drawString(200, y, str(int(qty)))
        p.drawString(330, y, f"{float(total):.2f}")
        y -= 20
        if y < 80:  
            p.showPage()
            y = height - 80

 
    y -= 20
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, f"Produto mais vendido: {best_seller}")
    y -= 20
    p.drawString(50, y, f"Total geral: R$ {overall:.2f}")

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer