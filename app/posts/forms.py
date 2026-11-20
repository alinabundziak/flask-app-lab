
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    BooleanField,
    DateTimeLocalField,
    SelectField,
    SelectMultipleField,
    SubmitField
)
from wtforms.validators import DataRequired, Length

from app.users.models import User
from app.posts.models import Tag


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

    author_id = SelectField(
        "Автор",
        coerce=int,
        validators=[DataRequired()]
    )

    tags = SelectMultipleField(
        "Теги",
        coerce=int
    )

    submit = SubmitField("Зберегти")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.author_id.choices = [
            (user.id, user.username)
            for user in User.query.order_by(User.id).all()
        ]

        self.tags.choices = [
            (tag.id, tag.name)
            for tag in Tag.query.order_by(Tag.name).all()
        ]
