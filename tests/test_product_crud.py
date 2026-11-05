
import unittest
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest.mock import patch

from tinydb import TinyDB

from app import create_app

app = create_app("testing")
from app.products import views


class ProductCRUDTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        db_path = Path(self.temp_dir.name) / "test_products.json"

        self.db = TinyDB(db_path)
        self.table = self.db.table("products")

        self.patcher = patch.object(
            views, "products_table", self.table
        )
        self.patcher.start()

        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False

        self.client = app.test_client()

    def tearDown(self):
        self.patcher.stop()
        self.db.close()
        self.temp_dir.cleanup()

    def test_product_list(self):
        response = self.client.get("/product")
        self.assertEqual(response.status_code, 200)

    def test_add_product(self):
        response = self.client.post(
            "/product/add",
            data={
                "name": "Laptop",
                "content": "Test laptop description",
                "price": "1200.50",
                "category": "electronics",
                "quantity": "5"
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.table.all()), 1)

    def test_product_detail(self):
        product_id = self.table.insert({
            "id": 1,
            "name": "Laptop",
            "content": "Test description",
            "price": "1200.50",
            "category": "electronics",
            "quantity": 5,
            "image": None,
            "created_at": "2026-11-04"
        })

        response = self.client.get(f"/product/{product_id}")
        self.assertEqual(response.status_code, 200)

    def test_edit_product(self):
        product_id = self.table.insert({
            "id": 1,
            "name": "Laptop",
            "content": "Test description",
            "price": "1200.50",
            "category": "electronics",
            "quantity": 5,
            "image": None,
            "created_at": "2026-11-04"
        })

        response = self.client.post(
            f"/product/{product_id}/edit",
            data={
                "name": "Updated Laptop",
                "content": "Updated description",
                "price": "1500.00",
                "category": "electronics",
                "quantity": "3"
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.table.get(doc_id=product_id)["name"],
            "Updated Laptop"
        )

    def test_delete_product(self):
        product_id = self.table.insert({
            "id": 1,
            "name": "Laptop",
            "content": "Test description",
            "price": "1200.50",
            "category": "electronics",
            "quantity": 5,
            "image": None,
            "created_at": "2026-11-04"
        })

        response = self.client.post(
            f"/product/{product_id}/delete",
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.table.all()), 0)

    def test_invalid_price(self):
        response = self.client.post(
            "/product/add",
            data={
                "name": "Laptop",
                "content": "Test description",
                "price": "-100",
                "category": "electronics",
                "quantity": "5"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.table.all()), 0)

    def test_negative_quantity(self):
        response = self.client.post(
            "/product/add",
            data={
                "name": "Laptop",
                "content": "Test description",
                "price": "100.00",
                "category": "electronics",
                "quantity": "-5"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.table.all()), 0)

    def test_nonexistent_product(self):
        response = self.client.get("/product/999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
