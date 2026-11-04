
from decimal import Decimal

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileSize
from wtforms import (
    StringField, TextAreaField, DecimalField,
    SelectField, IntegerField, SubmitField
)
from wtforms.validators import (
    DataRequired, Length, NumberRange,
    InputRequired, Optional, ValidationError
)


class ProductForm(FlaskForm):
    name = StringField(
        "Назва товару",
        validators=[
            DataRequired(),
            Length(min=3)
        ]
    )

    content = TextAreaField(
        "Опис",
        render_kw={"rows": 5, "cols": 40},
        validators=[DataRequired()]
    )

    price = DecimalField(
        "Ціна",
        places=2,
        validators=[
            InputRequired(),
            NumberRange(min=Decimal("0.01"))
        ]
    )

    category = SelectField(
        "Категорія",
        choices=[
            ("electronics", "Електроніка"),
            ("books", "Книги"),
            ("other", "Інше")
        ],
        validators=[DataRequired()]
    )

    quantity = IntegerField(
        "Кількість",
        validators=[
            InputRequired(),
            NumberRange(min=0)
        ]
    )

    image = FileField(
        "Зображення",
        validators=[
            Optional(),
            FileAllowed(
                ["png", "jpg", "jpeg"],
                "Дозволені PNG, JPG, JPEG"
            ),
            FileSize(
                max_size=2 * 1024 * 1024
            )
        ]
    )

    submit = SubmitField("Зберегти")

    def validate_price(self, field):
        if field.data is not None:
            if field.data.as_tuple().exponent < -2:
                raise ValidationError(
                    "Ціна може мати максимум 2 знаки після коми"
                )
