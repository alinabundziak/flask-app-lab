
from datetime import datetime

from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from app import db
from app.posts import post_bp
from app.posts.models import Post, Tag
from app.posts.forms import PostForm
from app.users.models import User


@post_bp.route("/")
def all_posts():
    posts = db.session.scalars(
        db.select(Post)
        .where(Post.is_active.is_(True))
        .order_by(Post.posted.desc())
    ).all()

    return render_template(
        "posts/all_posts.html",
        posts=posts
    )


@post_bp.route("/<int:id>")
def detail_post(id):
    post = db.get_or_404(Post, id)

    return render_template(
        "posts/detail_post.html",
        post=post
    )


@post_bp.route("/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        selected_user = db.get_or_404(
            User,
            form.author_id.data
        )

        selected_tags = db.session.scalars(
            db.select(Tag).where(
                Tag.id.in_(form.tags.data)
            )
        ).all() if form.tags.data else []

        post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            is_active=form.is_active.data,
            posted=form.publish_date.data,
            user_id=selected_user.id,
            author=selected_user.username
        )

        post.tags = selected_tags

        db.session.add(post)
        db.session.commit()

        flash("Пост успішно створено!", "success")
        return redirect(url_for("posts.all_posts"))

    if not form.is_submitted():
        form.publish_date.data = datetime.now().replace(
            second=0,
            microsecond=0
        )

    return render_template(
        "posts/add_post.html",
        form=form,
        title="Створення поста"
    )


@post_bp.route("/<int:id>/update", methods=["GET", "POST"])
def update_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)

    if form.validate_on_submit():
        selected_user = db.get_or_404(
            User,
            form.author_id.data
        )

        selected_tags = db.session.scalars(
            db.select(Tag).where(
                Tag.id.in_(form.tags.data)
            )
        ).all() if form.tags.data else []

        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.is_active = form.is_active.data
        post.posted = form.publish_date.data
        post.user_id = selected_user.id
        post.author = selected_user.username
        post.tags = selected_tags

        db.session.commit()

        flash("Пост успішно оновлено!", "success")
        return redirect(
            url_for("posts.detail_post", id=post.id)
        )

    if not form.is_submitted():
        form.publish_date.data = post.posted

        if post.user_id is not None:
            form.author_id.data = post.user_id

        form.tags.data = [tag.id for tag in post.tags]

    return render_template(
        "posts/add_post.html",
        form=form,
        title="Редагування поста",
        post=post
    )


@post_bp.route("/<int:id>/delete", methods=["GET", "POST"])
def delete_post(id):
    post = db.get_or_404(Post, id)

    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()

        flash("Пост успішно видалено!", "success")
        return redirect(url_for("posts.all_posts"))

    return render_template(
        "posts/delete_confirm.html",
        post=post
    )
