import enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

# Modelo usuario


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(
        String(50), unique=False, nullable=False)
    lastname: Mapped[str] = mapped_column(
        String(50), unique=False, nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)

    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")
    followers = relationship(
        "Follower", foreign_keys="[Follower.user_to_id]", back_populates="followed")
    following = relationship(
        "Follower", foreign_keys="[Follower.user_from_id]", back_populates="follower")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
        }

# Modelo media


class MediaType(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"


class Media(db.Model):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MediaType] = mapped_column(Enum(MediaType), nullable=False)
    url: Mapped[str] = mapped_column(String(120), nullable=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    post = relationship("Post", back_populates="media")

    def serialize(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "type": self.type.value,
            "url": self.url
        }


# Modelo post
class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    author = relationship("User", back_populates="posts")
    media = relationship("Media", back_populates="post",
                         cascade="all, delete-orphan")
    comments = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
        }


# Modelo comentario
class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(280), nullable=False)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id,
        }

# Modelo follower


class Follower(db.Model):
    __tablename__ = "follower"

    user_from_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), primary_key=True)

    follower = relationship("User", foreign_keys=[
                            user_from_id], back_populates="following")
    followed = relationship("User", foreign_keys=[
                            user_to_id], back_populates="followers")

    def serialize(self):
        return {
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id,
        }
