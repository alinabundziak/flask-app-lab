import logging
from pathlib import Path

from flask import (
    render_template, redirect, url_for, flash
)

from app import app
from app.forms import ContactForm
from flask import render_template, request
from app import app


@app.route("/")
@app.route("/resume")
def resume():
    return render_template("resume.html", title="Резюме")



@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        log_dir = Path(app.root_path).parent / "logs"
        log_dir.mkdir(exist_ok=True)

        logging.basicConfig(
            filename=log_dir / "contacts.log",
            level=logging.INFO,
            format="%(asctime)s - %(message)s"
        )

        try:
            logging.info(
                "Name: %s | Email: %s | Phone: %s | "
                "Subject: %s | Message: %s",
                form.name.data,
                form.email.data,
                form.phone.data,
                form.subject.data,
                form.message.data
            )

            flash(
                "Повідомлення успішно надіслано!",
                "success"
            )

        except OSError:
            flash(
                "Помилка під час запису повідомлення!",
                "danger"
            )

        return redirect(url_for("contact"))

    if form.is_submitted():
        flash(
            "Перевірте правильність заповнення форми!",
            "danger"
        )

    return render_template(
        "contact.html",
        title="Контакти",
        form=form
    )



@app.route("/homepage")
def home():
    return render_template("homepage.html", title="Головна")