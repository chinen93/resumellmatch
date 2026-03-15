import unittest

from sqlalchemy import create_engine

from src.storage.models import Base
from src.storage.repositories.user_repo import UserRepo


class TestUserRepo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use a test database
        cls.engine = create_engine("sqlite:///./output/test_storage.db", echo=False)
        Base.metadata.create_all(cls.engine)
        # Override the db instance for tests
        from src.storage import connection

        connection.DatabaseConnection._instance = None  # Reset singleton
        connection.DatabaseConnection._instance = connection.DatabaseConnection()
        connection.DatabaseConnection._instance.engine = cls.engine

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(cls.engine)

    def setUp(self):
        users = UserRepo.get_all_users()
        for user in users:
            UserRepo.delete_user(user.id)

    def test_create_user(self):
        user_id = UserRepo.create_user("Test User", "test@example.com")
        self.assertIsInstance(user_id, int)
        self.assertGreater(user_id, 0)

    def test_get_user_by_id(self):
        user_id = UserRepo.create_user("Test User", "test@example.com")
        user = UserRepo.get_user_by_id(user_id)
        self.assertIsNotNone(user)
        self.assertEqual(user.name, "Test User")
        self.assertEqual(user.email, "test@example.com")

    def test_get_user_by_id_not_found(self):
        user = UserRepo.get_user_by_id(999)
        self.assertIsNone(user)

    def test_get_all_users(self):
        UserRepo.create_user("User1", "user1@example.com")
        UserRepo.create_user("User2", "user2@example.com")
        users = UserRepo.get_all_users()
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0].name, "User1")
        self.assertEqual(users[1].name, "User2")

    def test_update_user(self):
        user_id = UserRepo.create_user("Old Name", "old@example.com")
        updated_user = UserRepo.update_user(
            user_id, name="New Name", email="new@example.com"
        )
        self.assertEqual(updated_user.name, "New Name")
        self.assertEqual(updated_user.email, "new@example.com")

    def test_update_user_partial(self):
        user_id = UserRepo.create_user("Test", "test@example.com")
        updated_user = UserRepo.update_user(user_id, name="Updated")
        self.assertEqual(updated_user.name, "Updated")
        self.assertEqual(updated_user.email, "test@example.com")

    def test_update_user_not_found(self):
        with self.assertRaises(ValueError):
            UserRepo.update_user(999, name="Fail")

    def test_delete_user(self):
        user_id = UserRepo.create_user("To Delete", "delete@example.com")
        result = UserRepo.delete_user(user_id)
        self.assertTrue(result)
        user = UserRepo.get_user_by_id(user_id)
        self.assertIsNone(user)

    def test_delete_user_not_found(self):
        with self.assertRaises(ValueError):
            UserRepo.delete_user(999)


if __name__ == "__main__":
    unittest.main()
