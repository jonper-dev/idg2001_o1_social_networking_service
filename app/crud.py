from sqlalchemy.orm import Session
from app.models.models import User, Post, Hashtag
from sqlalchemy import or_

###################
### -- USERS -- ###
###################
def get_users(db: Session):
    return db.query(User).all()

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, name: str, email: str, password: str):
    # Hash the password (this is a placeholder, use a proper hashing function in production)
    user = User(name=name, email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

## Update user
def update_user(db: Session, user_id: int, name: str, email: str, password: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    user.name = name
    user.email = email
    user.password = password  # You could also hash it here
    db.commit()
    db.refresh(user)
    return user

## Partial update user
def partial_update_user(db: Session, user_id: int, updates: dict):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    for key, value in updates.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def follow_user(db: Session, follower_id: int, followed_id: int):
    follower = db.query(User).get(follower_id)
    followed = db.query(User).get(followed_id)
    if followed not in follower.following:
        follower.following.append(followed)
        db.commit()
    return follower



###################
### -- POSTS -- ###
###################
def create_post(db: Session, post_data):
    from app.models.models import Post, Hashtag  # Avoid circular imports

    post = Post(
        content=post_data.content,
        user_id=post_data.user_id,
        reply_to_id=post_data.reply_to_id
    )

    # Handle hashtags (optional)
    for tag in post_data.hashtags:
        tag = tag.lower().strip()
        existing = db.query(Hashtag).filter(Hashtag.name == tag).first()
        if existing:
            post.hashtags.append(existing)
        else:
            new_tag = Hashtag(name=tag)
            db.add(new_tag)
            post.hashtags.append(new_tag)

    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def get_posts(db: Session):
    return db.query(Post).all()

def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

## Update post
def update_post(db: Session, post_id: int, content: str):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return None
    post.content = content
    post.edited = True
    db.commit()
    db.refresh(post)
    return post

## Partial update post
def partial_update_post(db: Session, post_id: int, updates: dict):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return None
    for key, value in updates.items():
        setattr(post, key, value)
    db.commit()
    db.refresh(post)
    return post

## Delete post
def delete_post(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return None
    db.delete(post)
    db.commit()
    return post

def like_post(db: Session, user_id: int, post_id: int):
    post = db.query(Post).get(post_id)
    user = db.query(User).get(user_id)
    if user not in post.likes:
        post.likes.append(user)
        db.commit()
    return post

def reply_to_post(db: Session, user_id: int, content: str, parent_id: int):
    return create_post(db, user_id=user_id, content=content, reply_to_id=parent_id)



####################
### -- SEARCH -- ###
####################
def search_posts(db: Session, query: str):
    return db.query(Post).filter(
        or_(
            Post.content.ilike(f"%{query}%"),
            Post.hashtags.any(Hashtag.name.ilike(f"%{query}%"))
        )
    ).all()

def search_hashtags(db: Session, tag: str):
    return db.query(Hashtag).filter(Hashtag.name.ilike(f"%{tag}%")).all()
