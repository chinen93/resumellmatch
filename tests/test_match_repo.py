import unittest

from src.storage.models import Base
from src.storage.repositories import (
    JobDescriptionParsedRepo,
    JobDescriptionRepo,
    MatchRepo,
    ResumeRepo,
    UserRepo,
)
from tests.conf_log_test import BaseTestCase


class TestMatchRepo(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.match_repo = MatchRepo(isTest=True)
        cls.job_desc_repo = JobDescriptionRepo(isTest=True)
        cls.job_desc_parsed_repo = JobDescriptionParsedRepo(isTest=True)
        cls.resume_repo = ResumeRepo(isTest=True)
        cls.user_repo = UserRepo(isTest=True)

        engine = cls.match_repo.db.engine
        assert engine is not None

        Base.metadata.create_all(engine)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        engine = cls.match_repo.db.engine
        assert engine is not None

        Base.metadata.drop_all(engine)

    def setUp(self):
        users = self.user_repo.get_all()
        for user in users:
            assert user.id is not None
            self.user_repo.delete(user.id)

        jobs_parsed = self.job_desc_parsed_repo.get_all()
        for job in jobs_parsed:
            assert job.id is not None
            self.job_desc_parsed_repo.delete(job.id)

        jobs = self.job_desc_repo.get_all()
        for job in jobs:
            assert job.id is not None
            self.job_desc_repo.delete(job.id)

        matches = self.match_repo.get_all()
        for match in matches:
            assert match.resume_id is not None
            assert match.job_description_parsed_id is not None
            self.match_repo.delete(match.resume_id, match.job_description_parsed_id)

        # Create test entities
        self.user_id = self.user_repo.create_from_fields(
            1, "Test User", "test@example.com"
        )
        self.resume_id = self.resume_repo.create_from_fields(
            1, self.user_id, "Resume text"
        )
        self.job_id = self.job_desc_repo.create_from_fields(
            1, "http://example.com", "Engineer", "Job text"
        )
        self.parsed_id = self.job_desc_parsed_repo.create_from_fields(
            1,
            self.job_id,
            "Summary",
            "skill1",
            "skill2",
            "keyword1",
            "hash",
            "response",
        )

    def test_create(self):
        result = self.match_repo.create_from_fields(
            self.resume_id, self.parsed_id, 85, "Good match"
        )
        self.assertTrue(result)

    def test_get_by_ids(self):
        self.match_repo.create_from_fields(
            self.resume_id, self.parsed_id, 85, "Good match"
        )
        match = self.match_repo.get_by_ids(self.resume_id, self.parsed_id)
        self.assertIsNotNone(match)
        assert match is not None
        self.assertEqual(match.score, 85)

    def test_get_match_not_found(self):
        match = self.match_repo.get_by_ids(999, 999)
        self.assertIsNone(match)

    def test_get_all(self):
        self.match_repo.create_from_fields(
            self.resume_id, self.parsed_id, 85, "Good match"
        )
        # Create another parsed job
        job_id2 = self.job_desc_repo.create_from_fields(
            2, "http://example2.com", "Manager", "Job text 2"
        )
        parsed_id2 = self.job_desc_parsed_repo.create_from_fields(
            2, job_id2, "Summary2", "skill3", "skill4", "keyword2", "hash2", "response2"
        )
        self.match_repo.create_from_fields(
            self.resume_id, parsed_id2, 90, "Better match"
        )
        matches = self.match_repo.get_all()
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0].score, 85)
        self.assertEqual(matches[1].score, 90)

    def test_get_all_by_resume_id(self):
        self.match_repo.create_from_fields(
            self.resume_id, self.parsed_id, 85, "Good match"
        )
        matches = self.match_repo.get_all_by_resume_id(self.resume_id)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].score, 85)

    def test_get_all_by_job_parsed_id(self):
        self.match_repo.create_from_fields(
            self.resume_id, self.parsed_id, 85, "Good match"
        )
        matches = self.match_repo.get_all_by_job_parsed_id(self.parsed_id)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].score, 85)

    def test_update(self):
        self.match_repo.create_from_fields(
            self.resume_id, self.parsed_id, 85, "Good match"
        )
        match = self.match_repo.get_by_ids(self.resume_id, self.parsed_id)
        self.assertIsNotNone(match)

        assert match is not None
        match.score = 95
        self.match_repo.create_or_update(match)
        updated_match = self.match_repo.get_by_ids(self.resume_id, self.parsed_id)

        assert updated_match is not None
        self.assertEqual(updated_match.score, 95)

    def test_update_not_found(self):
        result = self.match_repo.delete(999, 999)
        self.assertFalse(result)

    def test_delete(self):
        self.match_repo.create_from_fields(
            self.resume_id, self.parsed_id, 85, "Good match"
        )
        match = self.match_repo.get_by_ids(self.resume_id, self.parsed_id)
        self.assertIsNotNone(match)

        assert match is not None
        assert match.resume_id is not None
        assert match.job_description_parsed_id is not None
        result = self.match_repo.delete(
            match.resume_id, match.job_description_parsed_id
        )

        self.assertTrue(result)
        match = self.match_repo.get_by_ids(self.resume_id, self.parsed_id)
        self.assertIsNone(match)

    def test_delete_not_found(self):
        result = self.match_repo.delete(999, 999)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
