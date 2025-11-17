# -*- coding: utf-8 -*-
"""Event forms."""
from flask_wtf import FlaskForm
from wtforms import DateTimeField, StringField, TextAreaField
from wtforms.validators import DataRequired, Optional


class EventForm(FlaskForm):
    """Form for creating/editing an event."""

    title = StringField("Event Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[Optional()])
    start_date = DateTimeField(
        "Start Date & Time",
        validators=[DataRequired()],
        format="%Y-%m-%dT%H:%M"
    )
    end_date = DateTimeField(
        "End Date & Time",
        validators=[Optional()],
        format="%Y-%m-%dT%H:%M"
    )
    location = StringField("Location", validators=[Optional()])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(EventForm, self).__init__(*args, **kwargs)


class PostForm(FlaskForm):
    """Form for creating a timeline post."""

    content = TextAreaField("What's on your mind?", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(PostForm, self).__init__(*args, **kwargs)


class CommentForm(FlaskForm):
    """Form for commenting on a post."""

    content = TextAreaField("Add a comment", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(CommentForm, self).__init__(*args, **kwargs)
