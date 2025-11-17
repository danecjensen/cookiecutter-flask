# -*- coding: utf-8 -*-
"""Event views."""
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from community_calendar.database import db
from community_calendar.events.forms import CommentForm, EventForm, PostForm
from community_calendar.events.models import Comment, Event, Post

blueprint = Blueprint("events", __name__, url_prefix="/events", static_folder="../static")


@blueprint.route("/timeline")
@login_required
def timeline():
    """Timeline view - shows posts and comments."""
    post_form = PostForm()
    # Get all posts ordered by creation date (newest first)
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("events/timeline.html", posts=posts, post_form=post_form)


@blueprint.route("/timeline/post", methods=["POST"])
@login_required
def create_post():
    """Create a new timeline post."""
    form = PostForm()
    if form.validate_on_submit():
        post = Post(content=form.content.data, user_id=current_user.id)
        post.save()
        flash("Post created successfully!", "success")
    else:
        flash("Error creating post. Please try again.", "danger")
    return redirect(url_for("events.timeline"))


@blueprint.route("/timeline/post/<int:post_id>/comment", methods=["POST"])
@login_required
def create_comment(post_id):
    """Create a comment on a post."""
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            user_id=current_user.id,
            post_id=post.id
        )
        comment.save()
        flash("Comment added successfully!", "success")
    else:
        flash("Error adding comment. Please try again.", "danger")
    return redirect(url_for("events.timeline"))


@blueprint.route("/calendar")
@login_required
def calendar():
    """Calendar view - shows events in a calendar format."""
    event_form = EventForm()
    return render_template("events/calendar.html", event_form=event_form)


@blueprint.route("/api/events")
@login_required
def get_events():
    """API endpoint to get all events for the calendar."""
    events = Event.query.all()
    return jsonify([event.to_dict() for event in events])


@blueprint.route("/api/events/<int:event_id>")
@login_required
def get_event(event_id):
    """API endpoint to get a single event with its associated post."""
    event = Event.query.get_or_404(event_id)
    event_dict = event.to_dict()

    # Include the original post if it exists
    if event.post_id:
        post = Post.query.get(event.post_id)
        if post:
            event_dict['post'] = {
                'id': post.id,
                'content': post.content,
                'created_at': post.created_at.isoformat(),
                'user': {
                    'username': post.user.username,
                    'full_name': post.user.full_name,
                    'profile_image': post.user.profile_image
                },
                'comments': [{
                    'id': comment.id,
                    'content': comment.content,
                    'created_at': comment.created_at.isoformat(),
                    'user': {
                        'username': comment.user.username,
                        'full_name': comment.user.full_name,
                        'profile_image': comment.user.profile_image
                    }
                } for comment in post.comments]
            }

    return jsonify(event_dict)


@blueprint.route("/create", methods=["GET", "POST"])
@login_required
def create_event():
    """Create a new event."""
    form = EventForm()
    if form.validate_on_submit():
        # Create the event
        event = Event(
            title=form.title.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            location=form.location.data,
            user_id=current_user.id
        )

        # Create a timeline post for this event
        post_content = f"📅 New Event: {event.title}\n"
        if event.description:
            post_content += f"\n{event.description}\n"
        if event.location:
            post_content += f"\n📍 Location: {event.location}"

        post = Post(content=post_content, user_id=current_user.id)
        post.save()

        # Link the event to the post
        event.post_id = post.id
        event.save()

        # Link the post to the event
        post.event_id = event.id
        post.save()

        flash("Event created successfully!", "success")
        return redirect(url_for("events.calendar"))

    return render_template("events/create_event.html", form=form)


@blueprint.route("/edit/<int:event_id>", methods=["GET", "POST"])
@login_required
def edit_event(event_id):
    """Edit an existing event."""
    event = Event.query.get_or_404(event_id)

    # Check if the current user is the creator or an admin
    if event.user_id != current_user.id and not current_user.is_admin:
        flash("You don't have permission to edit this event.", "danger")
        return redirect(url_for("events.calendar"))

    form = EventForm(obj=event)

    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.start_date = form.start_date.data
        event.end_date = form.end_date.data
        event.location = form.location.data
        event.save()

        flash("Event updated successfully!", "success")
        return redirect(url_for("events.calendar"))

    return render_template("events/edit_event.html", form=form, event=event)


@blueprint.route("/delete/<int:event_id>", methods=["POST"])
@login_required
def delete_event(event_id):
    """Delete an event."""
    event = Event.query.get_or_404(event_id)

    # Check if the current user is the creator or an admin
    if event.user_id != current_user.id and not current_user.is_admin:
        flash("You don't have permission to delete this event.", "danger")
        return redirect(url_for("events.calendar"))

    event.delete()
    flash("Event deleted successfully!", "success")
    return redirect(url_for("events.calendar"))
