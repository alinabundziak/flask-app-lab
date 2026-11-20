
import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from app.config import config


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("APP_CONFIG", "development")

    app = Flask(__name__)

    app.config.from_object(config[config_name])
    app.config["SQLALCHEMY_ECHO"] = False

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "users.login"
    login_manager.login_message = "Увійдіть, щоб отримати доступ до цієї сторінки."
    login_manager.login_message_category = "warning"

    from app.users import user_bp
    from app.products import product_bp
    from app.posts import post_bp

    from app.posts.models import Post, Tag
    from app.products.models import Product, Category
    from app.users.models import User

    app.register_blueprint(user_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(post_bp)

    from app import views

    app.add_url_rule(
        "/",
        endpoint="index",
        view_func=views.resume
    )

    app.add_url_rule(
        "/resume",
        endpoint="resume",
        view_func=views.resume
    )

    app.add_url_rule(
        "/contact",
        endpoint="contact",
        view_func=views.contact,
        methods=["GET", "POST"]
    )

    app.add_url_rule(
        "/homepage",
        endpoint="home",
        view_func=views.home
    )

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    return app
