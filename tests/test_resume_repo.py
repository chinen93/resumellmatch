import unittest

from src.storage.models import Base
from src.storage.repositories.resume_repo import ResumeRepo
from src.storage.repositories.user_repo import UserRepo
from tests.conf_log_test import BaseTestCase


class TestResumeRepo(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Use a test database
        cls.resume_repo = ResumeRepo(isTest=True)
        cls.user_repo = UserRepo(isTest=True)

        Base.metadata.create_all(cls.resume_repo.db.engine)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        Base.metadata.drop_all(cls.resume_repo.db.engine)

    def setUp(self):
        resumes = self.resume_repo.get_all()
        for resume in resumes:
            self.resume_repo.delete(resume.id)

        users = self.user_repo.get_all()
        for user in users:
            self.user_repo.delete(user.id)

        self.user_id = self.user_repo.create("Test User", "test@example.com")

    def test_create(self):
        resume_id = self.resume_repo.create(self.user_id, "Resume text")
        self.assertIsInstance(resume_id, int)
        self.assertGreater(resume_id, 0)

    def test_get_by_id(self):
        resume_id = self.resume_repo.create(self.user_id, "Resume text")
        resume = self.resume_repo.get_by_id(resume_id)
        self.assertIsNotNone(resume)
        self.assertEqual(resume.raw_text, "Resume text")

    def test_get_by_id_not_found(self):
        resume = self.resume_repo.get_by_id(999)
        self.assertIsNone(resume)

    def test_get_all(self):
        self.resume_repo.create(self.user_id, "Resume 1")
        self.resume_repo.create(self.user_id, "Resume 2")
        resumes = self.resume_repo.get_all()
        self.assertEqual(len(resumes), 2)
        self.assertEqual(resumes[0].raw_text, "Resume 1")
        self.assertEqual(resumes[1].raw_text, "Resume 2")

    def test_get_all_by_user_id(self):
        self.resume_repo.create(self.user_id, "Resume 1")
        self.resume_repo.create(self.user_id, "Resume 2")
        resumes = self.resume_repo.get_all_by_user_id(self.user_id)
        self.assertEqual(len(resumes), 2)

    def test_update(self):
        resume_id = self.resume_repo.create(self.user_id, "Old text")
        updated_resume = self.resume_repo.update(resume_id, raw_text="New text")
        self.assertEqual(updated_resume.raw_text, "New text")

    def test_update_not_found(self):
        with self.assertRaises(ValueError):
            self.resume_repo.update(999, raw_text="Fail")

    def test_delete(self):
        resume_id = self.resume_repo.create(self.user_id, "Resume text")
        result = self.resume_repo.delete(resume_id)
        self.assertTrue(result)
        resume = self.resume_repo.get_by_id(resume_id)
        self.assertIsNone(resume)

    def test_delete_not_found(self):
        with self.assertRaises(ValueError):
            self.resume_repo.delete(999)


if __name__ == "__main__":
    unittest.main()
