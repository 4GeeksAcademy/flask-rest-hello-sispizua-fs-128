from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, column,ForeigKey
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    userName: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    firstName: Mapped[str] = mapped_column(String(120), nullable=False)
    lastName: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    


    def serialize(self):
        return {
            "id": self.id,
            "userName": self.userName,
            "firstName": self.firstName,
            "lastname": self.lastName,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Follower(db.Model):
    user_from_id: Mapped[int]=mapped_column(primary_key=True)
    user_to_id: Mapped[int]=mapped_column(int, nullable=False)

    def serialize(self):
        return{
            "user_from_id": self.user_from_id,
            "user_to_id":self.user_to_id
        }
    
class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[int]=mapped_column(int, nullable=False)

    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id
        }   
    

class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type:Mapped[str] =mapped_column(String(120), nullable=False)
    url: Mapped[str]=mapped_column(String(255), nullable=False)
    post_id:Mapped[int]=mapped_column(int, nullable=False )

    def serialize(self):
        return{
           "id": self.id,
           "type":self.type,
           "utl":self.url,
           "post_id":self.post_id
        }

class Commetn(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text:Mapped[str] =mapped_column(String(300), nullable=False)
    author_id: Mapped[int]=mapped_column(int, nullable=False)
    post_id:Mapped[int]=mapped_column(int, nullable=False)

    def serialize(self):
        return{
           "id": self.id,
           "comment_text":self.comment_text,
           "author_id":self.author_id,
           "post_id":self.post_id
        }

