from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

# Modelo usuario


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    nick: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="comment_author")
    stories = relationship("Story", back_populates="story_author")

    def serialize(self):
        return {
            "id": self.id,
            "nick": self.nick,
            "email": self.email,
            "is_active": self.is_active
        }


# Modelo post
class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column(String(8), nullable=False)
    caption: Mapped[str] = mapped_column(String(120), nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    author = relationship("User", back_populates="posts")

    comments = relationship("Comment", back_populates="post")  # 🔹 corregido

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "date": self.date,
            "caption": self.caption
        }


# Modelo comentario
class Comment(db.Model):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(120), nullable=True)
    like: Mapped[bool] = mapped_column(Boolean, nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    comment_author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "author_id": self.user_id,
            "post_id": self.post_id,
            "text": self.text,
            "like": self.like
        }


# Modelo story
class Story(db.Model):
    __tablename__ = "story"

    id: Mapped[int] = mapped_column(primary_key=True)
    like: Mapped[bool] = mapped_column(Boolean, nullable=True)
    views: Mapped[int] = mapped_column(Integer, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    story_author = relationship("User", back_populates="stories")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "like": self.like,
            "views": self.views
        }
