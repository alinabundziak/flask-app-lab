
import unittest

from app import create_app, db
from app.users.models import User


class AuthTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()

        self.context = self.app.app_context()
        self.context.push()

        db.create_all()

        self.user = User(
            username="testuser",
            email="testuser@example.com",
            password=""
        )

        self.user.hash_password("TestPass123!")

        db.session.add(self.user)
        db.session.commit()

        self.user_id = self.user.id

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    def login(self):
        return self.client.post(
            "/users/login",
            data={
                "email": "testuser@example.com",
                "password": "TestPass123!"
            },
            follow_redirects=True
        )

    def test_register_page(self):
        response = self.client.get("/users/register")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Реєстрація".encode(), response.data)

    def test_login_page(self):
        response = self.client.get("/users/login")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Вхід у систему".encode(), response.data)

    def test_register_user(self):
        response = self.client.post(
            "/users/register",
            data={
                "username": "newstudent",
                "email": "newstudent@example.com",
                "password": "NewPass123!",
                "confirm_password": "NewPass123!"
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)

        user = db.session.scalar(
            db.select(User).where(
                User.email == "newstudent@example.com"
            )
        )

        self.assertIsNotNone(user)
        self.assertTrue(user.check_password("NewPass123!"))
        self.assertNotEqual(user.password, "NewPass123!")

    def test_duplicate_registration(self):
        response = self.client.post(
            "/users/register",
            data={
                "username": "testuser",
                "email": "testuser@example.com",
                "password": "NewPass123!",
                "confirm_password": "NewPass123!"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Користувач із таким іменем уже існує.".encode(),
            response.data
        )

        self.assertEqual(
            db.session.query(User).count(),
            1
        )

    def test_successful_login(self):
        response = self.login()

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Мій профіль".encode(),
            response.data
        )

        self.assertIn(
            "testuser@example.com".encode(),
            response.data
        )

    def test_invalid_login(self):
        response = self.client.post(
            "/users/login",
            data={
                "email": "testuser@example.com",
                "password": "WrongPassword"
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Неправильна електронна пошта або пароль!".encode(),
            response.data
        )

        account_response = self.client.get("/users/account")
        self.assertEqual(account_response.status_code, 302)

    def test_logout(self):
        self.login()

        response = self.client.post(
            "/users/logout",
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Ви успішно вийшли із системи!".encode(),
            response.data
        )

        account_response = self.client.get("/users/account")
        self.assertEqual(account_response.status_code, 302)

    def test_protected_pages(self):
        account_response = self.client.get("/users/account")
        users_response = self.client.get("/users/all-users")

        self.assertEqual(account_response.status_code, 302)
        self.assertEqual(users_response.status_code, 302)

        self.assertIn(
            "/users/login",
            account_response.headers["Location"]
        )

    def test_all_users_page(self):
        self.login()

        response = self.client.get("/users/all-users")

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Усього користувачів: 1".encode(),
            response.data
        )

    def test_authenticated_register_redirect(self):
        self.login()

        response = self.client.get("/users/register")

        self.assertEqual(response.status_code, 302)
        self.assertIn(
            "/users/account",
            response.headers["Location"]
        )


if __name__ == "__main__":
    unittest.main()
