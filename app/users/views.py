
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

    return render_template(
        "users/profile.html",
        title="Профіль",
        username=session["username"]
    )


@user_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)

    flash("Ви успішно вийшли із системи!", "success")

    return redirect(url_for("users.login"))
