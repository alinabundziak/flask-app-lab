
import unittest
from datetime import datetime

from app import create_app, db
from app.posts.models import Post, Tag
from app.users.models import User


class PostTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()

        self.context = self.app.app_context()
        self.context.push()

        db.create_all()

        self.user = User(
            username="testuser",
            email="testuser@example.com",
            password="test-password"
        )

        self.python_tag = Tag(name="Python")
        self.flask_tag = Tag(name="Flask")

        db.session.add_all([
            self.user,
            self.python_tag,
            self.flask_tag
        ])
        db.session.commit()

        self.user_id = self.user.id
        self.python_tag_id = self.python_tag.id
        self.flask_tag_id = self.flask_tag.id

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    def create_post(self):
        post = Post(
            title="Тестовий пост",
            content="Тестовий вміст",
            category="news",
            posted=datetime.now(),
            is_active=True,
            author=self.user.username,
            user_id=self.user_id
        )

        db.session.add(post)
        db.session.commit()

        return post

    def test_posts_page(self):
        response = self.client.get("/post/")

        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        response = self.client.post(
            "/post/create",
            data={
                "title": "Новий пост",
                "content": "Текст нового поста",
                "category": "tech",
                "publish_date": "2026-11-05T12:00",
                "author_id": str(self.user_id),
                "tags": [
                    str(self.python_tag_id),
                    str(self.flask_tag_id)
                ],
                "is_active": "y"
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)

        post = db.session.scalar(
            db.select(Post).where(Post.title == "Новий пост")
        )

        self.assertIsNotNone(post)
        self.assertEqual(post.user_id, self.user_id)
        self.assertEqual(post.user.username, "testuser")
        self.assertCountEqual(
            [tag.name for tag in post.tags],
            ["Python", "Flask"]
        )

    def test_post_detail(self):
        post = self.create_post()

        response = self.client.get(f"/post/{post.id}")

        self.assertEqual(response.status_code, 200)

    def test_update_post(self):
        post = self.create_post()

        response = self.client.post(
            f"/post/{post.id}/update",
            data={
                "title": "Оновлений пост",
                "content": "Оновлений текст",
                "category": "publication",
                "publish_date": "2026-11-05T13:00",
                "author_id": str(self.user_id),
                "tags": [str(self.python_tag_id)],
                "is_active": "y"
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)

        updated_post = db.session.get(Post, post.id)

        self.assertEqual(updated_post.title, "Оновлений пост")
        self.assertEqual(updated_post.user_id, self.user_id)
        self.assertEqual(
            [tag.name for tag in updated_post.tags],
            ["Python"]
        )

    def test_delete_post(self):
        post = self.create_post()
        post_id = post.id

        response = self.client.post(
            f"/post/{post_id}/delete",
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(db.session.get(Post, post_id))

    def test_nonexistent_post(self):
        response = self.client.get("/post/99999")

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
