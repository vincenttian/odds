from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Table,
    DateTime,
    Text,
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import ARRAY

Base = declarative_base()

user_community_association = Table(
    "user_community",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("community_id", Integer, ForeignKey("communities.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    email_confirmed_at = Column(DateTime, nullable=True)
    password_confirmed_at = Column(DateTime, nullable=True)
    first_name = Column(String)
    last_name = Column(String)
    profile_photo = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    username = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=True)
    phone_verified_at = Column(DateTime, nullable=True)
    age = Column(Integer)
    school_id = Column(Integer, ForeignKey("communities.id"))

    # Relationships
    communities = relationship(
        "Community",
        secondary=user_community_association,
        backref="users",
    )
    following = relationship(
        "UserFollows",
        foreign_keys="[UserFollows.user_id]",
        backref="follower",
        cascade="all, delete-orphan",
    )
    followers = relationship(
        "UserFollows",
        foreign_keys="[UserFollows.following_user_id]",
        backref="following_user",
        cascade="all, delete-orphan",
    )
    challenges_created = relationship(
        "Challenge", foreign_keys="Challenge.creator_id", backref="creator"
    )
    challenges_participating = relationship(
        "Challenge",
        secondary="challenge_participants",
        backref="participants",
    )
    comments = relationship("Comment", backref="user")


class UserFollows(Base):
    __tablename__ = "user_follows"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    following_user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)


class Community(Base):
    __tablename__ = "communities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    country = Column(String)
    state = Column(String)
    city = Column(String)
    district = Column(String)
    zip_code = Column(String)
    zip_4 = Column(String)
    address = Column(String)
    population = Column(Integer)
    lat = Column(String)
    long = Column(String)
    phone = Column(String)
    website = Column(String)

    # Relationships (users relationship defined above)


challenge_participants = Table(
    "challenge_participants",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("challenge_id", Integer, ForeignKey("challenges.id"), primary_key=True),
)


class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    # opponent_ids = Column(ARRAY(Integer))  # Using ARRAY for PostgreSQL
    range_end = Column(Integer)  # Always starts at 1
    creator_number = Column(Integer, nullable=True)
    opponent_numbers = Column(ARRAY(Integer), nullable=True)  # Array for opponent numbers
    created_at = Column(DateTime)
    is_active = Column(Boolean, default=False)

    # Relationships (creator relationship defined above)
    comments = relationship("Comment", backref="challenge")
    re_rolls = relationship("ChallengeReRoll", backref="challenge")
    insurance = relationship("ChallengeInsurance", backref="challenge")


class ChallengeReRoll(Base):
    __tablename__ = "challenge_rerolls"

    id = Column(Integer, primary_key=True, index=True)
    challenge_id = Column(Integer, ForeignKey("challenges.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime)


class ChallengeInsurance(Base):
    __tablename__ = "challenge_insurance"

    id = Column(Integer, primary_key=True, index=True)
    challenge_id = Column(Integer, ForeignKey("challenges.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime)


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    challenge_id = Column(Integer, ForeignKey("challenges.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    created_at = Column(DateTime)