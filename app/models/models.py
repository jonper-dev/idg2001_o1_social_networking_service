from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, Boolean, DateTime, func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

## Many-to-many relationship for followers
followers = Table(
    'followers',
    Base.metadata,
    Column('follower_id', Integer, ForeignKey('users.id')),
    Column('followed_id', Integer, ForeignKey('users.id'))
)

## Many-to-many relationship for likes
likes = Table(
    'likes',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('post_id', Integer, ForeignKey('posts.id'))
)

## Many-to-many for hashtags
post_hashtags = Table(
    'post_hashtags',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id')),
    Column('hashtag_id', Integer, ForeignKey('hashtags.id'))
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True)
    password = Column(String(100))
    posts = relationship("Post", back_populates="author")
    following = relationship(
        "User",
        secondary=followers,
        primaryjoin=id==followers.c.follower_id,
        secondaryjoin=id==followers.c.followed_id,
        backref="followers"
    )

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=func.now())
    edited = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    reply_to_id = Column(Integer, ForeignKey('posts.id'), nullable=True)

    author = relationship("User", back_populates="posts")
    likes = relationship("User", secondary=likes, backref="liked_posts")
    hashtags = relationship("Hashtag", secondary=post_hashtags, back_populates="posts")
    replies = relationship("Post", remote_side=[id], backref="parent")

class Hashtag(Base):
    __tablename__ = 'hashtags'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    posts = relationship("Post", secondary=post_hashtags, back_populates="hashtags")

#################################################################
### -- Pydantic models for request and response validation -- ###
#################################################################
## These models are used to validate the data sent to and from the API.

#############
### Users ###
#############
## Used for creating a new user
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

## Used for updating a user (full update)
class UserUpdate(BaseModel):
    name: str
    email: str
    password: str

## Used for partial update (PATCH)
class UserPatch(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

#############
### Posts ###
#############
## Used for creating a new post
class PostCreate(BaseModel):
    content: str
    user_id: int
    reply_to_id: Optional[int] = None
    hashtags: Optional[list[str]] = []

## Used for a partial update (PATCH)
class PostPatch(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
