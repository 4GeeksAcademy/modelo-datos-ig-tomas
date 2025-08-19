from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

# Modelo usuario


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

# Modelo post


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[str] = mapped_column(foreign_key=True)
    date: Mapped[str] = mapped_column(String(8), unique=False, nullable=False)
    caption: Mapped[str] = mapped_column(String(120), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "date": self.date,
            "caption": self.caption,
        }

# Modelo comentario


class Coment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[str] = mapped_column(foreign_key=True)
    text: Mapped[str] = mapped_column(String(120), unique=False, nullable=True)
    like: Mapped[bool] = mapped_column(Boolean, nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "text": self.text,
            "like": self.like,
        }

# Modelo storys


class Story(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[str] = mapped_column(foreign_key=True)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "is_active": self.is_active
        }
