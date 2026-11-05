
import logging
from pathlib import Path

from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    current_app
)

from app.forms import ContactForm


def resume():
    return render_template(
        "resume.html",
        title="Резюме"
    )


def contact():
    form = ContactForm()

    if form.validate_on_submit():
        log_dir = Path(current_app.root_path).parent / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / "contacts.log"

        try:
            logger = logging.getLogger("contacts")
            logger.setLevel(logging.INFO)

            if not logger.handlers:
                handler = logging.FileHandler(
                    log_file,
                    encoding="utf-8"
                )

                handler.setFormatter(
                    logging.Formatter(
                        "%(asctime)s - %(message)s"
                    )
                )

                logger.addHandler(handler)

            logger.info(
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


def home():
    return render_template(
        "homepage.html",
        title="Головна"
    )
