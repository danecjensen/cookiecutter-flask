# -*- coding: utf-8 -*-
"""User views."""
import os
from werkzeug.utils import secure_filename
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from community_calendar.user.forms import ProfileForm
from community_calendar.user.models import User

blueprint = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")


@blueprint.route("/")
@login_required
def members():
    """List members."""
    return render_template("users/members.html")


@blueprint.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Edit user profile."""
    form = ProfileForm(obj=current_user)

    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data

        # Handle profile image upload
        if form.profile_image.data:
            file = form.profile_image.data
            filename = secure_filename(file.filename)
            # Create unique filename to avoid collisions
            unique_filename = f"{current_user.id}_{filename}"

            # Ensure upload directory exists
            upload_dir = os.path.join(current_app.static_folder, "uploads", "profiles")
            os.makedirs(upload_dir, exist_ok=True)

            # Save the file
            file_path = os.path.join(upload_dir, unique_filename)
            file.save(file_path)

            # Store relative path in database
            current_user.profile_image = f"/static/uploads/profiles/{unique_filename}"

        current_user.save()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("user.profile"))

    return render_template("users/profile.html", form=form)
