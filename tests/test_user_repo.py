import unittest

from src.storage.models import Base
from src.storage.repositories import UserRepo
from tests.conf_log_test import BaseTestCase


class TestUserRepo(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_repo = UserRepo(isTest=True)

        engine = cls.user_repo.db.engine
        assert engine is not None

        Base.metadata.create_all(engine)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        engine = cls.user_repo.db.engine
        assert engine is not None

        Base.metadata.drop_all(engine)

    def setUp(self):
        users = self.user_repo.get_all()
        for user in users:
            assert user.id is not None
            self.user_repo.delete(user.id)

    def test_create(self):
        user_id = self.user_repo.create_from_fields(1, "Test User", "test@example.com")
        self.assertIsInstance(user_id, int)
        self.assertGreater(user_id, 0)

    def test_get_by_id(self):
        user_id = self.user_repo.create_from_fields(1, "Test User", "test@example.com")
        user = self.user_repo.get_by_id(user_id)
        assert user is not None

        self.assertEqual(user.name, "Test User")
        self.assertEqual(user.email, "test@example.com")

    def test_get_by_id_not_found(self):
        user = self.user_repo.get_by_id(999)
        self.assertIsNone(user)

    def test_get_all(self):
        self.user_repo.create_from_fields(3, "User1", "user1@example.com")
        self.user_repo.create_from_fields(4, "User2", "user2@example.com")
        users = self.user_repo.get_all()

        self.assertEqual(len(users), 2)
        self.assertEqual(users[0].name, "User1")
        self.assertEqual(users[1].name, "User2")

    def test_update(self):
        user_id = self.user_repo.create_from_fields(1, "Old Name", "old@example.com")
        user = self.user_repo.get_by_id(user_id)

        assert user is not None
        user.name = "New Name"
        user.email = "new@example.com"
        self.user_repo.create_or_update(user)

        updated_user = self.user_repo.get_by_id(user_id)
        assert updated_user is not None

        self.assertEqual(updated_user.name, "New Name")
        self.assertEqual(updated_user.email, "new@example.com")

    def test_update_partial(self):
        user_id = self.user_repo.create_from_fields(2, "Test", "test@example.com")
        user = self.user_repo.get_by_id(user_id)

        assert user is not None
        user.name = "Updated"
        self.user_repo.create_or_update(user)

        updated_user = self.user_repo.get_by_id(user_id)
        assert updated_user is not None

        self.assertEqual(updated_user.name, "Updated")
        self.assertEqual(updated_user.email, "test@example.com")

    def test_update_not_found(self):
        result = self.user_repo.delete(999)
        self.assertFalse(result)

    def test_delete(self):
        user_id = self.user_repo.create_from_fields(
            1, "To Delete", "delete@example.com"
        )
        result = self.user_repo.delete(user_id)
        self.assertTrue(result)

        user = self.user_repo.get_by_id(user_id)
        self.assertIsNone(user)

    def test_delete_not_found(self):
        result = self.user_repo.delete(999)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
