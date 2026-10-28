from flask import Flask

app = Flask(__name__)

from app import views
from app.users import user_bp
from app.products import product_bp

app.register_blueprint(user_bp)
app.register_blueprint(product_bp)