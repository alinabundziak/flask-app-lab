
from datetime import datetime, timezone

from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    session,
    request
)

from app import db
from app.posts import post_bp
from app.posts.models import Post
from app.posts.forms import PostForm


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
        post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            is_active=form.is_active.data,
            posted=form.publish_date.data,
            author=session.get("username", "Anonymous")
        )

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
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.is_active = form.is_active.data
        post.posted = form.publish_date.data

        db.session.commit()

        flash("Пост успішно оновлено!", "success")
        return redirect(
            url_for("posts.detail_post", id=post.id)
        )

    if not form.is_submitted():
        form.publish_date.data = post.posted

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
