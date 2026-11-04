
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from tinydb import TinyDB

from app import app
from app.products import views


class ProductTestCase(unittest.TestCase):

    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        db_path = Path(self.temp_dir.name) / "products.json"

        self.db = TinyDB(db_path)
        self.table = self.db.table("products")

        self.patcher = patch.object(
            views,
            "products_table",
            self.table
        )
        self.patcher.start()

        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False

        self.client = app.test_client()

    def tearDown(self):
        self.patcher.stop()
        self.db.close()
        self.temp_dir.cleanup()

    def test_products_page(self):
        response = self.client.get("/product")
        self.assertEqual(response.status_code, 200)

    def test_product_detail(self):
        product_id = self.table.insert({
            "id": 1,
            "name": "Laptop",
            "content": "Test laptop",
            "price": "1200.00",
            "category": "electronics",
            "quantity": 5,
            "image": None,
            "created_at": "2026-11-04"
        })

        response = self.client.get(
            f"/product/{product_id}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)

    def test_invalid_product(self):
        response = self.client.get("/product/999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
