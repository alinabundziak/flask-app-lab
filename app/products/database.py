
from pathlib import Path
from tinydb import TinyDB

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

db = TinyDB(DATA_DIR / "products.json")
products_table = db.table("products")
