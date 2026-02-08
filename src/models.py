from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Column, ForeignKey, Table, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()
#tabla suplementaria para la relacion muchos a muchos
followers =Table(
    "followers",
    db.Model.metadata,
    db.Column("user_from_id", Integer, ForeignKey("user.id"),primary_key=True),
    db.Column("user_to_id", Integer, ForeignKey("user.id"),primary_key=True)

)

class User(db.Model):
    __tablename__= "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    userName: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    firstName: Mapped[str] = mapped_column(String(120), nullable=False)
    lastName: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    #Codigo para las relaciones
    following: Mapped[list["User"]]= relationship(
        "User",
        secondary =followers,
        primaryjoin=(id == followers.c.user_from_id),
        secondaryjoin=(id == followers.c.user_to_id),
        backref="followers"
    )
    Posts: Mapped[list["Post"]] = relationship(back_populates ="user")
    Comment: Mapped[list["Comment"]] =relationship(back_populates="user")
    


    def serialize(self):
        return {
            "id": self.id,
            "userName": self.userName,
            "firstName": self.firstName,
            "lastname": self.lastName,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

    
class Post(db.Model):
    __tablename__ ="post"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[int]=mapped_column(ForeignKey("user.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post")
    media: Mapped[list["Media"]] = relationship(back_populates="post")

    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
             "media":[m.serialize() for m in self.media],
            "comments": [c.serialize() for c in self.comments]
        }   
    

class Media(db.Model):
    __tablename__="media"
    id: Mapped[int] = mapped_column(primary_key=True)
    type:Mapped[str] =mapped_column(String(120), nullable=False)
    url: Mapped[str]=mapped_column(String(255), nullable=False)
    post_id:Mapped[int]=mapped_column(ForeignKey("post.id"), nullable=False )

    post:Mapped["Post"]=relationship(back_populates="media")

    def serialize(self):
        return{
           "id": self.id,
           "type":self.type,
           "url":self.url,
           "post_id":self.post_id
        }

class Comment(db.Model):
    __tablename__="comment"
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text:Mapped[str] =mapped_column(String(300), nullable=False)
    author_id: Mapped[int]=mapped_column(ForeignKey("user.id"), nullable=False)
    post_id:Mapped[int]=mapped_column(ForeignKey("post.id"), nullable=False)

    post:Mapped["User"]= relationship(back_populates="comments")
    post: Mapped["Post"]=relationship(back_populates="comments")

    def serialize(self):
        return{
           "id": self.id,
           "comment_text":self.comment_text,
           "author_id":self.author_id,
           "post_id":self.post_id
        }

