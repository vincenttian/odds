import uuid
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
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.sql import func

Base = declarative_base()

user_community_association = Table(
    "user_community",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("community_id", UUID(as_uuid=True), ForeignKey("communities.id"), primary_key=True),
)

class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class User(Base, TimestampMixin):
    __tablename__ = "users"

    # id = Column(Integer, primary_key=True, index=True)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    email_confirmed_at = Column(DateTime, nullable=True)
    password_confirmed_at = Column(DateTime, nullable=True)
    first_name = Column(String)
    last_name = Column(String)
    profile_photo = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    username = Column(String, unique=True, nullable=True)
    phone_number = Column(String, nullable=True)
    phone_verified_at = Column(DateTime(timezone=True), nullable=True)
    age = Column(Integer)
    school_id = Column(UUID(as_uuid=True), ForeignKey("communities.id"))

    verification_code = Column(String, nullable=True)
    verification_code_created_at = Column(DateTime(timezone=True), nullable=True, server_default=func.now())
    is_verified = Column(Boolean, default=False)
    
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


class UserFollows(Base, TimestampMixin):
    __tablename__ = "user_follows"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    following_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)


class Community(Base, TimestampMixin):
    __tablename__ = "communities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
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
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("challenge_id", UUID(as_uuid=True), ForeignKey("challenges.id"), primary_key=True),
)


class Challenge(Base, TimestampMixin):
    __tablename__ = "challenges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    creator_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    # opponent_ids = Column(ARRAY(Integer))  # Using ARRAY for PostgreSQL
    range_end = Column(Integer)  # Always starts at 1
    creator_number = Column(Integer, nullable=True)
    opponent_numbers = Column(ARRAY(Integer), nullable=True)  # Array for opponent numbers
    is_active = Column(Boolean, default=False)

    # Relationships (creator relationship defined above)
    comments = relationship("Comment", backref="challenge")
    re_rolls = relationship("ChallengeReRoll", backref="challenge")
    insurance = relationship("ChallengeInsurance", backref="challenge")


class ChallengeReRoll(Base, TimestampMixin):
    __tablename__ = "challenge_rerolls"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    challenge_id = Column(UUID(as_uuid=True), ForeignKey("challenges.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))


class ChallengeInsurance(Base, TimestampMixin):
    __tablename__ = "challenge_insurance"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    challenge_id = Column(UUID(as_uuid=True), ForeignKey("challenges.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))


class Comment(Base, TimestampMixin):
    __tablename__ = "comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    challenge_id = Column(UUID(as_uuid=True), ForeignKey("challenges.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    content = Column(Text)