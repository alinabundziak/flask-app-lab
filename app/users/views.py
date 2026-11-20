
import re

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    make_response
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from . import user_bp
from app import db
from app.forms import RegistrationForm, LoginForm
from app.users.models import User


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


@user_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip().lower(),
            password=""
        )

        user.hash_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash(
            "Реєстрація успішна! Тепер увійдіть у систему.",
            "success"
        )

        return redirect(url_for("users.login"))

    return render_template(
        "users/register.html",
        title="Реєстрація",
        form=form
    )


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        password = form.password.data

        user = db.session.scalar(
            db.select(User).where(User.email == email)
        )

        if user and user.check_password(password):
            login_user(
                user,
                remember=form.remember.data
            )

            session["username"] = user.username

            flash(
                "Ви успішно увійшли в систему!",
                "success"
            )

            return redirect(url_for("users.account"))

        flash(
            "Неправильна електронна пошта або пароль!",
            "danger"
        )

    return render_template(
        "users/login.html",
        title="Вхід",
        form=form
    )


@user_bp.route("/account")
@login_required
def account():
    return render_template(
        "users/account.html",
        title="Мій профіль",
        user=current_user
    )


@user_bp.route("/all-users")
@login_required
def all_users():
    users = db.session.scalars(
        db.select(User).order_by(User.id)
    ).all()

    return render_template(
        "users/all_users.html",
        title="Список користувачів",
        users=users
    )


@user_bp.route("/profile")
@login_required
def profile():
    cookies = dict(request.cookies)

    theme = request.cookies.get(
        "profile_theme",
        "dark"
    )

    if theme not in ("light", "dark"):
        theme = "dark"

    return render_template(
        "users/profile.html",
        title="Профіль",
        username=current_user.username,
        cookies=cookies,
        theme=theme
    )


@user_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    session.pop("username", None)

    flash(
        "Ви успішно вийшли із системи!",
        "success"
    )

    return redirect(url_for("users.login"))


@user_bp.route("/add-cookie", methods=["POST"])
@login_required
def add_cookie():
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
@login_required
def delete_cookie():
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
@login_required
def delete_all_cookies():
    response = make_response(
        redirect(url_for("users.profile"))
    )

    for key in request.cookies:
        if key.startswith("lab4_"):
            response.delete_cookie(key)

    flash(
        "Усі додані cookie видалено!",
        "success"
    )

    return response


@user_bp.route("/theme/<string:theme>")
@login_required
def change_theme(theme):
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
