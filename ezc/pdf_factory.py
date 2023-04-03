from typing import List, Tuple

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle


class PdfFactory:
    def __init__(self, filename: str) -> None:
        self.doc = SimpleDocTemplate(filename)
        self.elements = []

    def generate_shopping_list(self, ingredients: List[Tuple[str]]) -> None:
        self._add_title("Shopping list")
        categories = ("Name", "Category", "Shelf", "Quantity", "Unit Price")
        # Insert categories at the beginning of the ingredients list

        data = [categories] + ingredients
        self._add_table(data)
        self._generate()

    def _add_title(self, title: str) -> None:
        title_style = getSampleStyleSheet()["Heading1"]
        title_style.alignment = TA_CENTER
        title_style.spaceAfter = 40
        title_style.fontSize = 25
        self.elements.append(Paragraph(title, title_style))

    def _add_table(self, table_data: list) -> None:
        table_style = TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BOX", (0, 0), (-1, -1), 3, colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 15),
                ("FONT", (0, 1), (-1, -1), "Helvetica", 15),
            ]
        )
        table = Table(data=table_data)
        table.setStyle(table_style)
        self.elements.append(table)

    def _generate(self) -> None:
        self.doc.build(self.elements)