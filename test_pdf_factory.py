import unittest
from unittest import TestCase

from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table

from pdf_factory import PdfFactory


class PdfFactoryTest(TestCase):
    def test_create_pdf_factory(self):
        # Arrange
        pdf_factory = PdfFactory("test.pdf")

        # Assert
        self.assertIsInstance(pdf_factory.doc, SimpleDocTemplate)
        self.assertEqual(pdf_factory.doc.filename, "test.pdf")
        self.assertEqual(pdf_factory.elements, [])

    def test_add_title(self):
        # Arrange
        pdf_factory = PdfFactory("test.pdf")
        title = "My title"

        # Act
        pdf_factory.add_title(title)

        # Assert
        self.assertEqual(len(pdf_factory.elements), 1)
        self.assertIsInstance(pdf_factory.elements[0], Paragraph)
        self.assertEqual(pdf_factory.elements[0].text, title)
        self.assertEqual(pdf_factory.elements[0].style.name, "Heading1")
        self.assertEqual(pdf_factory.elements[0].style.alignment, TA_CENTER)
        self.assertEqual(pdf_factory.elements[0].style.spaceBefore, 0)
        self.assertEqual(pdf_factory.elements[0].style.spaceAfter, 40)
        self.assertEqual(pdf_factory.elements[0].style.fontSize, 25)

    def test_add_table(self):
        # Arrange
        pdf_factory = PdfFactory("test.pdf")
        table_data = [
            ("Nom", "Category", "Shelf", "Quantity", "Unit price"),
            ("Banana", "Market", "Fruits and Vegetable", "4kg", "4€"),
            ("Onion", "Market", "Fruits and Vegetable", "2kg", "3€"),
            ("Yaourt", "Supermarket", "Milk products", "500g", "2 €"),
            ("Milk", "Supermarket", "Milk products", "6kg", "0.9"),
            ("Bread", "Market", "Baker", "3", "0.8€"),
        ]

        # Act
        pdf_factory.add_table(table_data)

        # Assert
        self.assertEqual(len(pdf_factory.elements), 1)
        self.assertIsInstance(pdf_factory.elements[0], Table)
        for data_line in table_data:
            for data in data_line:
                self.assertIn(data, str(pdf_factory.elements[0]))


if __name__ == "__main__":
    unittest.main()
