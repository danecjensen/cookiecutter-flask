# -*- coding: utf-8 -*-
"""Event models."""
import datetime as dt

from community_calendar.database import Column, PkModel, db, reference_col, relationship


class Event(PkModel):
    """An event in the community calendar."""

    __tablename__ = "events"
    title = Column(db.String(200), nullable=False)
    description = Column(db.Text, nullable=True)
    start_date = Column(db.DateTime, nullable=False)
    end_date = Column(db.DateTime, nullable=True)
    location = Column(db.String(255), nullable=True)
    created_at = Column(
        db.DateTime, nullable=False, default=dt.datetime.now(dt.timezone.utc)
    )
    updated_at = Column(
        db.DateTime, nullable=False, default=dt.datetime.now(dt.timezone.utc),
        onupdate=dt.datetime.now(dt.timezone.utc)
    )

    # Foreign key to the user who created the event
    user_id = reference_col("users", nullable=False)
    user = relationship("User", backref="events")

    # Foreign key to the original post (timeline post)
    post_id = reference_col("posts", nullable=True)

    def __init__(self, title, start_date, user_id, **kwargs):
        """Create instance."""
        super().__init__(title=title, start_date=start_date, user_id=user_id, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Event({self.title!r})>"

    def to_dict(self):
        """Convert event to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'start': self.start_date.isoformat() if self.start_date else None,
            'end': self.end_date.isoformat() if self.end_date else None,
            'location': self.location,
            'user_id': self.user_id,
            'post_id': self.post_id,
        }


class Post(PkModel):
    """A timeline post about an event or general discussion."""

    __tablename__ = "posts"
    content = Column(db.Text, nullable=False)
    created_at = Column(
        db.DateTime, nullable=False, default=dt.datetime.now(dt.timezone.utc)
    )
    updated_at = Column(
        db.DateTime, nullable=False, default=dt.datetime.now(dt.timezone.utc),
        onupdate=dt.datetime.now(dt.timezone.utc)
    )

    # Foreign key to the user who created the post
    user_id = reference_col("users", nullable=False)
    user = relationship("User", backref="posts")

    # Optional: link to an event if this post is about an event
    event_id = reference_col("events", nullable=True)
    event = relationship("Event", backref="posts", foreign_keys=[event_id])

    def __init__(self, content, user_id, **kwargs):
        """Create instance."""
        super().__init__(content=content, user_id=user_id, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Post(id={self.id}, user_id={self.user_id})>"


class Comment(PkModel):
    """A comment on a post."""

    __tablename__ = "comments"
    content = Column(db.Text, nullable=False)
    created_at = Column(
        db.DateTime, nullable=False, default=dt.datetime.now(dt.timezone.utc)
    )
    updated_at = Column(
        db.DateTime, nullable=False, default=dt.datetime.now(dt.timezone.utc),
        onupdate=dt.datetime.now(dt.timezone.utc)
    )

    # Foreign key to the user who created the comment
    user_id = reference_col("users", nullable=False)
    user = relationship("User", backref="comments")

    # Foreign key to the post being commented on
    post_id = reference_col("posts", nullable=False)
    post = relationship("Post", backref="comments")

    def __init__(self, content, user_id, post_id, **kwargs):
        """Create instance."""
        super().__init__(content=content, user_id=user_id, post_id=post_id, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Comment(id={self.id}, post_id={self.post_id})>"
