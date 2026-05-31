import unittest

from src.storage.models import Base
from src.storage.repositories import JobDescriptionParsedRepo, JobDescriptionRepo
from tests.conf_log_test import BaseTestCase


class TestJobDescriptionRepo(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.job_desc_repo = JobDescriptionRepo(isTest=True)

        engine = cls.job_desc_repo.db.engine
        assert engine is not None

        Base.metadata.create_all(engine)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        engine = cls.job_desc_repo.db.engine
        assert engine is not None

        Base.metadata.drop_all(engine)

    def setUp(self):
        jobs = self.job_desc_repo.get_all()
        for job in jobs:
            assert job.id is not None
            self.job_desc_repo.delete(job.id)

    def test_create(self):
        job_id = self.job_desc_repo.create_from_fields(
            1, "http://example.com", "Engineer", "Job text"
        )
        self.assertIsInstance(job_id, int)
        self.assertGreater(job_id, 0)

    def test_get_by_id(self):
        job_id = self.job_desc_repo.create_from_fields(
            1, "http://example.com", "Engineer", "Job text"
        )
        job = self.job_desc_repo.get_by_id(job_id)
        self.assertIsNotNone(job)
        assert job is not None
        self.assertEqual(job.title, "Engineer")

    def test_get_by_id_not_found(self):
        job = self.job_desc_repo.get_by_id(999)
        self.assertIsNone(job)

    def test_get_all(self):
        self.job_desc_repo.create_from_fields(
            1, "http://example.com", "Engineer", "Job text"
        )
        self.job_desc_repo.create_from_fields(
            2, "http://example2.com", "Manager", "Job text 2"
        )
        jobs = self.job_desc_repo.get_all()
        self.assertEqual(len(jobs), 2)
        self.assertEqual(jobs[0].title, "Engineer")
        self.assertEqual(jobs[1].title, "Manager")

    def test_update(self):
        job_id = self.job_desc_repo.create_from_fields(
            1, "http://example.com", "Engineer", "Job text"
        )
        job = self.job_desc_repo.get_by_id(job_id)
        self.assertIsNotNone(job)

        assert job is not None
        job.title = "Senior Engineer"
        self.job_desc_repo.create_or_update(job)
        updated_job = self.job_desc_repo.get_by_id(job_id)

        assert updated_job is not None
        self.assertEqual(updated_job.title, "Senior Engineer")

    def test_update_not_found(self):
        result = self.job_desc_repo.delete(999)
        self.assertFalse(result)

    def test_delete(self):
        job_id = self.job_desc_repo.create_from_fields(
            1, "http://example.com", "Engineer", "Job text"
        )
        result = self.job_desc_repo.delete(job_id)
        self.assertTrue(result)
        job = self.job_desc_repo.get_by_id(job_id)
        self.assertIsNone(job)

    def test_delete_not_found(self):
        result = self.job_desc_repo.delete(999)
        self.assertFalse(result)


class TestJobDescriptionParsedRepo(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.job_desc_repo = JobDescriptionRepo(isTest=True)
        cls.job_desc_parsed_repo = JobDescriptionParsedRepo(isTest=True)

        engine = cls.job_desc_parsed_repo.db.engine
        assert engine is not None

        Base.metadata.create_all(engine)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

        engine = cls.job_desc_parsed_repo.db.engine
        assert engine is not None

        Base.metadata.drop_all(engine)

    def setUp(self):
        jobs_parsed = self.job_desc_parsed_repo.get_all()
        for job in jobs_parsed:
            assert job.id is not None
            self.job_desc_parsed_repo.delete(job.id)

        jobs = self.job_desc_repo.get_all()
        for job in jobs:
            assert job.id is not None
            self.job_desc_repo.delete(job.id)

    def test_create(self):
        job_id = self.job_desc_repo.create_from_fields(
            1, "http://example.com", "Engineer", "Job text"
        )
        parsed_id = self.job_desc_parsed_repo.create_from_fields(
            1,
            job_id,
            "Summary",
            "skill1,skill2",
            "skill3",
            "keyword1,keyword2",
            "hash123",
            "full response",
        )
        self.assertIsInstance(parsed_id, int)
        self.assertGreater(parsed_id, 0)

    def test_get_by_id(self):
        job_id = self.job_desc_repo.create_from_fields(
            1, "http://example.com", "Engineer", "Job text"
        )
        parsed_id = self.job_desc_parsed_repo.create_from_fields(
            1,
            job_id,
            "Summary",
            "skill1,skill2",
            "skill3",
            "keyword1,keyword2",
            "hash123",
            "full response",
        )
        parsed = self.job_desc_parsed_repo.get_by_id(parsed_id)
        self.assertIsNotNone(parsed)
        assert parsed is not None
        self.assertEqual(parsed.summary, "Summary")

    def test_get_by_job_id(self):
        job_id = self.job_desc_repo.create_from_fields(
            1, "http://example.com", "Engineer", "Job text"
        )
        _ = self.job_desc_parsed_repo.create_from_fields(
            1,
            job_id,
            "Summary",
            "skill1,skill2",
            "skill3",
            "keyword1,keyword2",
            "hash123",
            "full response",
        )
        parsed = self.job_desc_parsed_repo.get_by_job_id(job_id)
        self.assertIsNotNone(parsed)
        assert parsed is not None
        self.assertEqual(parsed.summary, "Summary")

    def test_get_all(self):
        job_id1 = self.job_desc_repo.create_from_fields(
            1, "http://example.com", "Engineer", "Job text"
        )
        self.job_desc_parsed_repo.create_from_fields(
            1,
            job_id1,
            "Summary1",
            "skill1",
            "skill2",
            "keyword1",
            "hash1",
            "response1",
        )
        job_id2 = self.job_desc_repo.create_from_fields(
            2, "http://example2.com", "Manager", "Job text 2"
        )
        self.job_desc_parsed_repo.create_from_fields(
            2,
            job_id2,
            "Summary2",
            "skill3",
            "skill4",
            "keyword2",
            "hash2",
            "response2",
        )
        parseds = self.job_desc_parsed_repo.get_all()
        self.assertEqual(len(parseds), 2)
        self.assertEqual(parseds[0].summary, "Summary1")
        self.assertEqual(parseds[1].summary, "Summary2")

    def test_update(self):
        job_id = self.job_desc_repo.create_from_fields(
            1, "http://example.com", "Engineer", "Job text"
        )
        parsed_id = self.job_desc_parsed_repo.create_from_fields(
            1,
            job_id,
            "Summary",
            "skill1,skill2",
            "skill3",
            "keyword1,keyword2",
            "hash123",
            "full response",
        )
        parsed = self.job_desc_parsed_repo.get_by_id(parsed_id)
        self.assertIsNotNone(parsed)

        assert parsed is not None
        parsed.summary = "Updated Summary"
        self.job_desc_parsed_repo.create_or_update(parsed)
        updated_parsed = self.job_desc_parsed_repo.get_by_id(parsed_id)

        assert updated_parsed is not None
        self.assertEqual(updated_parsed.summary, "Updated Summary")

    def test_update_not_found(self):
        result = self.job_desc_parsed_repo.delete(999)
        self.assertFalse(result)

    def test_delete(self):
        job_id = self.job_desc_repo.create_from_fields(
            1, "http://example.com", "Engineer", "Job text"
        )
        parsed_id = self.job_desc_parsed_repo.create_from_fields(
            1,
            job_id,
            "Summary",
            "skill1,skill2",
            "skill3",
            "keyword1,keyword2",
            "hash123",
            "full response",
        )
        result = self.job_desc_parsed_repo.delete(parsed_id)
        self.assertTrue(result)
        parsed = self.job_desc_parsed_repo.get_by_id(parsed_id)
        self.assertIsNone(parsed)

    def test_delete_not_found(self):
        result = self.job_desc_parsed_repo.delete(999)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
