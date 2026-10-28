from flask import render_template, request
from app import app


@app.route("/")
@app.route("/resume")
def resume():
    return render_template("resume.html", title="Резюме")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    message = None

    if request.method == "POST":
        message = "Дякую! Це демонстраційна форма, тому повідомлення не надсилається."

    return render_template(
        "contact.html",
        title="Контакти",
        message=message
    )


@app.route("/homepage")
def home():
    return render_template("homepage.html", title="Головна")