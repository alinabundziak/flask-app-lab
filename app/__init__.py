
import os
from flask import Flask

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "dev-only-lab4-secret"
)

from app import views
from app.users import user_bp
from app.products import product_bp

app.register_blueprint(user_bp)
app.register_blueprint(product_bp)
