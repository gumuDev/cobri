from openpyxl import Workbook
from io import BytesIO

class ExcelGenerator:
    def __init__(self, items):
        self.items = items

    def generate_excel(self, title):
        wb = Workbook()
        ws = wb.active
        ws.title = f"Reporte de {title}"

        # Definir encabezados
        headers = ["Item", "Precio", "Cantidad", "Total"]
        ws.append(headers)

        # Agregar los datos
        for item in self.items:
            item_name = item.get("item")
            price = item.get("price")
            quantity = 0 if item.get("quantity") is None else item.get("quantity")
            total = price * quantity
            ws.append([item_name, price, quantity, total])

        file_stream = BytesIO()
        wb.save(file_stream)
        file_stream.seek(0)

        return file_stream