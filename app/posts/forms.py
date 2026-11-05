
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    BooleanField,
    DateTimeLocalField,
    SelectField,
    SubmitField
)
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField(
        "Назва поста",
        validators=[
            DataRequired(),
            Length(max=150)
        ]
    )

    content = TextAreaField(
        "Вміст поста",
        validators=[DataRequired()]
    )

    is_active = BooleanField(
        "Активний пост",
        default=True
    )

    publish_date = DateTimeLocalField(
        "Дата публікації",
        format="%Y-%m-%dT%H:%M",
        validators=[DataRequired()]
    )

    category = SelectField(
        "Категорія",
        choices=[
            ("news", "Новини"),
            ("publication", "Публікація"),
            ("tech", "Технології"),
            ("other", "Інше")
        ],
        default="other"
    )

    submit = SubmitField("Зберегти")
