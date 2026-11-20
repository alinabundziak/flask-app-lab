
from flask_login import UserMixin
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db, bcrypt, login_manager


@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except (ValueError, TypeError):
        return None


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
        unique=True
    )

    email: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        unique=True
    )

    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def hash_password(self, password):
        self.password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(
            self.password,
            password
        )

    def __repr__(self):
        return f"<User {self.username}>"
