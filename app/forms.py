
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    TextAreaField,
    PasswordField,
    BooleanField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    Regexp,
    EqualTo,
    ValidationError
)

from app.users.models import User


class ContactForm(FlaskForm):
    name = StringField(
        "Ім'я",
        validators=[
            DataRequired(),
            Length(min=4, max=10)
        ]
    )

    email = StringField(
        "Електронна пошта",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    phone = StringField(
        "Телефон",
        validators=[
            DataRequired(),
            Regexp(
                r"^\+380\d{9}$",
                message="Формат: +380XXXXXXXXX"
            )
        ]
    )

    subject = SelectField(
        "Тема",
        choices=[
            ("question", "Запитання"),
            ("suggestion", "Пропозиція"),
            ("other", "Інше")
        ],
        validators=[DataRequired()]
    )

    message = TextAreaField(
        "Повідомлення",
        validators=[
            DataRequired(),
            Length(max=500)
        ]
    )

    submit = SubmitField("Надіслати")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Ім'я користувача",
        validators=[
            DataRequired(),
            Length(min=4, max=16),
            Regexp(
                r"^[A-Za-z0-9_.]+$",
                message="Використовуй латинські літери, цифри, крапку або підкреслення."
            )
        ]
    )

    email = StringField(
        "Електронна пошта",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Пароль",
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )

    confirm_password = PasswordField(
        "Підтвердження пароля",
        validators=[
            DataRequired(),
            EqualTo(
                "password",
                message="Паролі повинні збігатися."
            )
        ]
    )

    submit = SubmitField("Зареєструватися")

    def validate_username(self, username):
        existing_user = User.query.filter_by(
            username=username.data
        ).first()

        if existing_user:
            raise ValidationError(
                "Користувач із таким іменем уже існує."
            )

    def validate_email(self, email):
        existing_user = User.query.filter_by(
            email=email.data
        ).first()

        if existing_user:
            raise ValidationError(
                "Користувач із такою електронною поштою вже існує."
            )


class LoginForm(FlaskForm):
    email = StringField(
        "Електронна пошта",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Пароль",
        validators=[
            DataRequired()
        ]
    )

    remember = BooleanField("Запам'ятати мене")

    submit = SubmitField("Увійти")
