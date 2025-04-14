from sqlalchemy.orm import Session
from models import User, Tweet, Hashtag
from sqlalchemy import or_

# --- USERS ---

def get_users(db: Session):
    return db.query(User).all()

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, name: str, email: str):
    user = User(name=name, email=email)
    db.add(user)
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

# --- POSTS/TWEETS ---

def create_tweet(db: Session, user_id: int, content: str, hashtags: list[str] = [], reply_to_id: int = None):
    tweet = Tweet(content=content, user_id=user_id, reply_to_id=reply_to_id)

    # Process hashtags
    for tag in hashtags:
        tag = tag.lower()
        existing = db.query(Hashtag).filter(Hashtag.name == tag).first()
        if existing:
            tweet.hashtags.append(existing)
        else:
            new_tag = Hashtag(name=tag)
            db.add(new_tag)
            tweet.hashtags.append(new_tag)

    db.add(tweet)
    db.commit()
    db.refresh(tweet)
    return tweet

def get_tweets(db: Session):
    return db.query(Tweet).all()

def get_tweet(db: Session, tweet_id: int):
    return db.query(Tweet).filter(Tweet.id == tweet_id).first()

def edit_tweet(db: Session, tweet_id: int, new_content: str):
    tweet = db.query(Tweet).get(tweet_id)
    tweet.content = new_content
    tweet.edited = True
    db.commit()
    db.refresh(tweet)
    return tweet

def like_tweet(db: Session, user_id: int, tweet_id: int):
    tweet = db.query(Tweet).get(tweet_id)
    user = db.query(User).get(user_id)
    if user not in tweet.likes:
        tweet.likes.append(user)
        db.commit()
    return tweet

def reply_to_tweet(db: Session, user_id: int, content: str, parent_id: int):
    return create_tweet(db, user_id=user_id, content=content, reply_to_id=parent_id)

# --- SEARCH ---

def search_tweets(db: Session, query: str):
    return db.query(Tweet).filter(
        or_(
            Tweet.content.ilike(f"%{query}%"),
            Tweet.hashtags.any(Hashtag.name.ilike(f"%{query}%"))
        )
    ).all()

def search_hashtags(db: Session, tag: str):
    return db.query(Hashtag).filter(Hashtag.name.ilike(f"%{tag}%")).all()