
import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.config import config


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("APP_CONFIG", "development")

    app = Flask(__name__)

    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    from app.users import user_bp
    from app.products import product_bp
    from app.posts import post_bp
    from app.posts.models import Post

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
