
from datetime import datetime
from decimal import Decimal
from io import BytesIO
from pathlib import Path
from uuid import uuid4

from flask import (
    render_template, redirect, url_for,
    flash, abort, request
)
from flask_wtf import FlaskForm
from PIL import Image
from tinydb import Query
from werkzeug.datastructures import FileStorage

from . import product_bp
from .forms import ProductForm
from .database import products_table


UPLOAD_DIR = Path(__file__).parent / "static" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_image(image):
    if not isinstance(image, FileStorage) or not image.filename:
        return None

    image_bytes = image.read()

    if len(image_bytes) > 2 * 1024 * 1024:
        raise ValueError("Зображення завелике")

    try:
        with Image.open(BytesIO(image_bytes)) as img:
            img.verify()

        with Image.open(BytesIO(image_bytes)) as img:
            image_format = img.format

    except Exception:
        raise ValueError("Некоректний файл зображення")

    extensions = {
        "PNG": "png",
        "JPEG": "jpg"
    }

    if image_format not in extensions:
        raise ValueError("Дозволені лише PNG, JPG, JPEG")

    filename = f"{uuid4().hex}.{extensions[image_format]}"
    filepath = UPLOAD_DIR / filename

    filepath.write_bytes(image_bytes)

    return f"uploads/{filename}"


def get_product(product_id):
    product = products_table.get(
        Query().id == product_id
    )

    if product is None:
        abort(404)

    return product


@product_bp.route("")
@product_bp.route("/")
def product_list():
    products = products_table.all()

    return render_template(
        "products/products.html",
        title="Товари",
        products=products
    )


@product_bp.route("/<int:product_id>")
def product_detail(product_id):
    product = get_product(product_id)

    delete_form = FlaskForm()

    return render_template(
        "products/detail_product.html",
        title=product["name"],
        product=product,
        delete_form=delete_form
    )


@product_bp.route("/add", methods=["GET", "POST"])
def add_product():
    form = ProductForm()

    if form.validate_on_submit():
        try:
            image_path = save_image(form.image.data)

        except (ValueError, OSError) as error:
            flash(str(error), "danger")

            return render_template(
                "products/product_form.html",
                title="Додати товар",
                form=form
            )

        product_data = {
            "name": form.name.data,
            "content": form.content.data,
            "price": str(form.price.data),
            "category": form.category.data,
            "quantity": form.quantity.data,
            "image": image_path,
            "created_at": datetime.now().isoformat(
                timespec="seconds"
            )
        }

        product_id = products_table.insert(product_data)

        products_table.update(
            {"id": product_id},
            doc_ids=[product_id]
        )

        flash("Товар успішно додано!", "success")

        return redirect(
            url_for("products.product_list")
        )

    return render_template(
        "products/product_form.html",
        title="Додати товар",
        form=form
    )


@product_bp.route(
    "/<int:product_id>/edit",
    methods=["GET", "POST"]
)
def edit_product(product_id):
    product = get_product(product_id)

    form_data = {
        **product,
        "price": Decimal(product["price"]),
        "image": None
    }

    form = ProductForm(data=form_data)

    if form.validate_on_submit():
        image_path = product.get("image")

        if isinstance(form.image.data, FileStorage) and form.image.data.filename:
            try:
                image_path = save_image(form.image.data)

            except (ValueError, OSError) as error:
                flash(str(error), "danger")

                return render_template(
                    "products/product_form.html",
                    title="Редагувати товар",
                    form=form
                )

        updated_data = {
            "name": form.name.data,
            "content": form.content.data,
            "price": str(form.price.data),
            "category": form.category.data,
            "quantity": form.quantity.data,
            "image": image_path
        }

        products_table.update(
            updated_data,
            Query().id == product_id
        )

        flash("Товар успішно оновлено!", "success")

        return redirect(
            url_for(
                "products.product_detail",
                product_id=product_id
            )
        )

    return render_template(
        "products/product_form.html",
        title="Редагувати товар",
        form=form
    )


@product_bp.route(
    "/<int:product_id>/delete",
    methods=["POST"]
)
def delete_product(product_id):
    form = FlaskForm()

    if not form.validate_on_submit():
        flash(
            "Помилка перевірки запиту!",
            "danger"
        )

        return redirect(
            url_for("products.product_list")
        )

    get_product(product_id)

    products_table.remove(
        Query().id == product_id
    )

    flash("Товар успішно видалено!", "success")

    return redirect(
        url_for("products.product_list")
    )
