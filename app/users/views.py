import re

from flask import (
    render_template, request, redirect,
    url_for, session, flash, make_response
)
from . import user_bp


@user_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, type=int)

    return render_template(
        "users/hi.html",
        title="Привітання",
        name=name,
        age=age
    )


@user_bp.route("/admin")
def admin():
    return redirect(
        url_for(
            "users.greetings",
            name="administrator",
            age=45
        )
    )

@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "student" and password == "12345":
            session["username"] = username

            flash("Вхід успішний!", "success")

            return redirect(url_for("users.profile"))

        flash("Неправильний логін або пароль!", "danger")
        return redirect(url_for("users.login"))

    return render_template("users/login.html", title="Вхід")



@user_bp.route("/profile")
def profile():
    if "username" not in session:
        flash("Спочатку увійдіть у систему!", "warning")
        return redirect(url_for("users.login"))

    cookies = dict(request.cookies)

    theme = request.cookies.get("profile_theme", "dark")

    if theme not in ("light", "dark"):
        theme = "dark"

    return render_template(
        "users/profile.html",
        title="Профіль",
        username=session["username"],
        cookies=cookies,
        theme=theme
    )



@user_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)

    flash("Ви успішно вийшли із системи!", "success")

    return redirect(url_for("users.login"))


@user_bp.route("/add-cookie", methods=["POST"])
def add_cookie():
    if "username" not in session:
        flash("Спочатку увійдіть!", "warning")
        return redirect(url_for("users.login"))

    key = request.form.get("key", "").strip()
    value = request.form.get("value", "")
    minutes = request.form.get("minutes", type=int)

    if not re.fullmatch(r"[A-Za-z0-9_]+", key):
        flash("Некоректний ключ cookie!", "danger")
        return redirect(url_for("users.profile"))

    if minutes is None or minutes <= 0:
        flash("Вкажіть додатний термін дії!", "danger")
        return redirect(url_for("users.profile"))

    response = make_response(
        redirect(url_for("users.profile"))
    )

    response.set_cookie(
        "lab4_" + key,
        value,
        max_age=minutes * 60,
        httponly=True,
        samesite="Lax"
    )

    flash("Cookie успішно додано!", "success")
    return response


@user_bp.route("/delete-cookie", methods=["POST"])
def delete_cookie():
    if "username" not in session:
        flash("Спочатку увійдіть!", "warning")
        return redirect(url_for("users.login"))

    key = request.form.get("key", "").strip()

    if not re.fullmatch(r"[A-Za-z0-9_]+", key):
        flash("Некоректний ключ cookie!", "danger")
        return redirect(url_for("users.profile"))

    response = make_response(
        redirect(url_for("users.profile"))
    )

    response.delete_cookie("lab4_" + key)

    flash("Cookie видалено!", "success")
    return response


@user_bp.route("/delete-all-cookies", methods=["POST"])
def delete_all_cookies():
    if "username" not in session:
        flash("Спочатку увійдіть!", "warning")
        return redirect(url_for("users.login"))

    response = make_response(
        redirect(url_for("users.profile"))
    )

    for key in request.cookies:
        if key.startswith("lab4_"):
            response.delete_cookie(key)

    flash("Усі додані cookie видалено!", "success")
    return response

@user_bp.route("/theme/<string:theme>")
def change_theme(theme):
    if "username" not in session:
        flash("Спочатку увійдіть!", "warning")
        return redirect(url_for("users.login"))

    if theme not in ("light", "dark"):
        flash("Невідома кольорова схема!", "danger")
        return redirect(url_for("users.profile"))

    response = make_response(
        redirect(url_for("users.profile"))
    )

    response.set_cookie(
        "profile_theme",
        theme,
        max_age=30 * 24 * 60 * 60,
        httponly=True,
        samesite="Lax"
    )

    flash("Тему успішно змінено!", "success")
    return response
