from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

# Modelo usuario


class User(db.Model):
    __tablename__ = "User"

    id: Mapped[int] = mapped_column(primary_key=True)
    nick: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "nick": self.nick,
            "email": self.email,
            "is_active": self.is_active

        }

# Modelo post


class Post(db.Model):
    __tablename__ = "Post"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column(String(8), unique=False, nullable=False)
    caption: Mapped[str] = mapped_column(String(120), nullable=True)

    user_id: Mapped[str] = mapped_column(ForeignKey("User.id"), nullable=False)
    user: Mapped[list["User"]] = relationShip(back_populate="Post")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "date": self.date,
            "caption": self.caption,
        }

# Modelo comentario


class Coment(db.Model):
    __tablename__ = "Coment"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(120), unique=False, nullable=True)
    like: Mapped[bool] = mapped_column(Boolean, nullable=True)

    user_id: Mapped[str] = mapped_column(ForeignKey("User.id"), nullable=False)
    user: Mapped[list["User"]] = relationShip(back_populate="Coment")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "text": self.text,
            "like": self.like,
        }

# Modelo storys


class Story(db.Model):
    __tablename__ = "Story"
    id: Mapped[int] = mapped_column(primary_key=True)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    like: Mapped[bool] = mapped_column(Boolean, nullable=True)

    user_id: Mapped[str] = mapped_column(ForeignKey("User.id"), nullable=False)
    user: Mapped[list["User"]] = relationShip(back_populate="Story")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "is_active": self.is_active,
            "like": self.like
        }

# Modelo follower


class Follower(db.Model):
    __tablename__ = "Follower"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[str] = mapped_column(ForeignKey("User.id"), nullable=False)
    user: Mapped[list["User"]] = relationShip(back_populate="Follower")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
        }
